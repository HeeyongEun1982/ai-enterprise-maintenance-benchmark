/* Controlled assertion replay, NOT an official Jest/container benchmark run.
 * Uses the published test bodies and their mock factories, with a small explicit
 * adapter for the assertion/mock APIs actually used by this one test file.
 * The migration function and request builders are extracted from the pinned gold
 * patch. Node's built-in TypeScript stripping removes types only.
 */
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const {stripTypeScriptTypes} = require('node:module');
const ROOT = __dirname;
const ID = 'instance_protonmail__webclients-2f2f6c311c6128fe86976950d3c0c2db07b03921';
const folder = path.join(ROOT,'sources');
const gold = fs.readFileSync(path.join(folder,'solution__gold_patch.diff'),'utf8');
const testsPath = path.join(folder,'published_useShareActions.test.ts');
const originalTests = fs.readFileSync(testsPath,'utf8');
const body = originalTests.replace(/^import[\s\S]*?;\s*$/gm,'');
const added = gold.split('\n').filter(x=>x.startsWith('+')&&!x.startsWith('+++')).map(x=>x.slice(1)).join('\n');
const start = added.indexOf('    const migrateShares = useCallback(');
const end = added.indexOf('\n    );',start)+'\n    );'.length;
if(start<0||end<start) throw Error('Migration extraction failed');
const migrationTs = added.slice(start,end);
const apiStart = added.indexOf('export const queryUnmigratedShares');
const apiTs = added.slice(apiStart).replace(/export const /g,'const ');
const apiJs = stripTypeScriptTypes(apiTs,{mode:'strip'});
const canonical = value => {
  if(Array.isArray(value)) return value.map(canonical);
  if(value&&typeof value==='object') return Object.fromEntries(Object.keys(value).filter(k=>value[k]!==undefined).sort().map(k=>[k,canonical(value[k])]));
  return value;
};
const equal = (a,b)=>JSON.stringify(canonical(a))===JSON.stringify(canonical(b));

function environment(migrationJs){
  const mocks=[], modules={}, collected=[], afters=[], traces={};
  function fn(implementation){
    let impl=implementation; const once=[];
    const f=function(...args){ f.mock.calls.push(args); const next=once.shift(); return (next||impl)?.(...args); };
    f.mock={calls:[]}; mocks.push(f);
    f.mockImplementation=x=>(impl=x,f);
    f.mockReturnValue=x=>(impl=()=>x,f);
    f.mockResolvedValue=x=>(impl=()=>Promise.resolve(x),f);
    f.mockResolvedValueOnce=x=>(once.push(()=>Promise.resolve(x)),f);
    f.mockRejectedValueOnce=x=>(once.push(()=>Promise.reject(x)),f);
    return f;
  }
  modules['../_api']={useDebouncedRequest:fn()};
  modules['@proton/shared/lib/calendar/crypto/encrypt']={getEncryptedSessionKey:fn()};
  const jest={fn,mocked:x=>x,mock:(name,factory)=>{if(factory)modules[name]=factory();},
    clearAllMocks:()=>mocks.forEach(f=>{f.mock.calls=[];}),requireActual:name=>{
      if(name!=='@proton/shared/lib/api/drive/share')throw Error('Unexpected requireActual '+name);
      return actualApi;
    }};
  let assertionCount=0;
  function expect(actual){
    const matchers=negated=>({
      toEqual(expected){assertionCount++;if(equal(actual,expected)===negated)throw Error('toEqual mismatch');},
      toHaveBeenCalledWith(...expected){assertionCount++;const ok=actual.mock.calls.some(a=>equal(a,expected));if(ok===negated)throw Error('toHaveBeenCalledWith mismatch');},
      toHaveBeenCalled(){assertionCount++;if((actual.mock.calls.length>0)===negated)throw Error('toHaveBeenCalled mismatch');}
    });
    return Object.assign(matchers(false),{not:matchers(true)});
  }
  const context={jest,expect,describe:(_name,cb)=>cb(),it:(name,cb)=>collected.push({name,cb}),afterEach:cb=>afters.push(cb),
    renderHook:hook=>({result:{current:hook()}}),HTTP_STATUS_CODE:{NOT_FOUND:404},
    uint8ArrayToBase64String:x=>Buffer.from(x).toString('base64'),AbortController,Promise,Uint8Array,console};
  for(const [name,module,member] of [['queryMigrateLegacyShares','@proton/shared/lib/api/drive/share','queryMigrateLegacyShares'],['getEncryptedSessionKey','@proton/shared/lib/calendar/crypto/encrypt','getEncryptedSessionKey'],['useDebouncedRequest','../_api','useDebouncedRequest']]){
    Object.defineProperty(context,name,{get:()=>modules[module][member]});
  }
  vm.createContext(context);
  const actualApi = vm.runInContext(`(()=>{${apiJs};return {queryUnmigratedShares,queryMigrateLegacyShares}})()`,context);
  context.useShareActions=()=>{
    const share = modules['./useShare'].default();
    const links = modules['../_links'].useLink();
    traces.links=links;
    const local={...context,debouncedRequest:modules['../_api'].useDebouncedRequest(),...share,...links,
      queryUnmigratedShares:modules['@proton/shared/lib/api/drive/share'].queryUnmigratedShares,
      queryMigrateLegacyShares:modules['@proton/shared/lib/api/drive/share'].queryMigrateLegacyShares,
      getEncryptedSessionKey:modules['@proton/shared/lib/calendar/crypto/encrypt'].getEncryptedSessionKey,
      useCallback:cb=>cb,chunk:(items,size)=>{const out=[];for(let i=0;i<(items?.length||0);i+=size)out.push(items.slice(i,i+size));return out;}};
    return vm.runInNewContext(`(()=>{${migrationJs};return {migrateShares}})()`,local);
  };
  vm.runInContext(body,context,{filename:'published-useShareActions.test.ts'});
  return {collected,afters,assertKeyBinding:()=>expect(modules['@proton/shared/lib/calendar/crypto/encrypt'].getEncryptedSessionKey).toHaveBeenCalledWith('sessionKey','privateKey'),trace:()=>({assertions:assertionCount,root_key_lookups:traces.links?.getLinkPrivateKey.mock.calls.length||0,
    encryption_calls:modules['@proton/shared/lib/calendar/crypto/encrypt'].getEncryptedSessionKey.mock.calls.length,
    encryption_keys:modules['@proton/shared/lib/calendar/crypto/encrypt'].getEncryptedSessionKey.mock.calls.map(c=>String(c[1]))})};
}

async function replay(label,migrationJs,strengthenKeyCheck=false){
  const first=environment(migrationJs),results=[];
  for(let i=0;i<first.collected.length;i++){
    const env=environment(migrationJs),test=env.collected[i];
    let status='PASSED',error;
    try{await Promise.race([test.cb(),new Promise((_,rej)=>setTimeout(()=>rej(Error('test timeout')),2000))]);
      if(strengthenKeyCheck && test.name==='migrateShares'){
        env.assertKeyBinding();
      }
    }
    catch(e){status='FAILED';error=String(e);}
    results.push({name:test.name,status,error,...env.trace()});
    for(const after of env.afters)await after();
  }
  return {variant:label,passed:results.filter(r=>r.status==='PASSED').length,total:results.length,tests:results};
}

(async()=>{
  const baselineJs=stripTypeScriptTypes(migrationTs,{mode:'strip'});
  const needle='getLinkPrivateKey(abortSignal, share.shareId, share.rootLinkId, true)';
  if(!baselineJs.includes(needle))throw Error('Mutation target not found');
  const mutantJs=baselineJs.replace(needle,'Promise.resolve(undefined)');
  fs.writeFileSync(path.join(ROOT,'proton_reference_migration.js'),baselineJs+'\n');
  fs.writeFileSync(path.join(ROOT,'proton_omit_root_key_migration.js'),mutantJs+'\n');
  const noSubmissionJs=baselineJs.replace('queryMigrateLegacyShares({','queryUnmigratedShares({');
  const results=[await replay('published_gold_migration_extracted',baselineJs),await replay('root_link_private_key_lookup_omitted',mutantJs),
    await replay('negative_control_submission_builder_omitted',noSubmissionJs),
    await replay('reference_with_added_key_binding_assertion',baselineJs,true),
    await replay('mutant_with_added_key_binding_assertion',mutantJs,true)];
  const record={scope:'Controlled replay of original published test bodies with explicit small mock/assertion/React-hook adapters; NOT official Jest, container or parser execution.',
    instance_id:ID,test_source_sha256:crypto.createHash('sha256').update(originalTests).digest('hex'),
    adapter_limits:['renderHook is a one-shot hook call; React lifecycle is not reproduced','Only the mock/assertion APIs used by this test file are implemented','chunk and base64 helpers are explicit local adapters','TypeScript is stripped; no project typecheck, workspace/module resolution or official verifier/parser run'],results};
  fs.writeFileSync(path.join(ROOT,'proton_key_oracle_replay.json'),JSON.stringify(record,null,2)+'\n');
  console.log(JSON.stringify(results.map(r=>({variant:r.variant,passed:r.passed,total:r.total,failed:r.tests.filter(t=>t.status!=='PASSED').map(t=>({name:t.name,error:t.error}))})),null,2));
})().catch(e=>{console.error(e);process.exitCode=1;});
