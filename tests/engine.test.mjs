import { test } from 'node:test';
import assert from 'node:assert/strict';
import { initialState, transition, generateRound, roleFor, randomIndex, WORDS } from '../src/engine.ts';

test('curated library has at least 150 unique words with broad one-word hints', () => {
  assert.ok(WORDS.length >= 150); assert.equal(new Set(WORDS.map(e => e.word)).size, WORDS.length);
  for (const {word,hint} of WORDS) {
    assert.match(word,/^[A-Z]+(?:-[A-Z]+)?$/); assert.match(hint,/^[A-Z]+$/);
    assert.notEqual(word,hint); assert.ok(!word.includes(hint));
  }
});
test('default, bounds, invalid counts and invalid transitions', () => {
  assert.equal(initialState().count,4);
  for (const count of [null,0,2,21,Infinity,NaN,4.5,'4']) assert.equal(initialState(count).count,4);
  const s=initialState();
  for (const type of ['HIDE','REVEAL','ANSWER','NEW_ROUND','SETUP']) assert.equal(transition(s,{type}),s);
  assert.equal(transition(s,{type:'COUNT',count:3}).count,3);
  assert.equal(transition(s,{type:'COUNT',count:20}).count,20);
  assert.equal(transition(s,{type:'COUNT',count:21}),s);
  assert.throws(()=>generateRound(2));
});
test('rejection sampling rejects biased tail, handles singleton, and fallback works', () => {
  let calls=0;
  const source={getRandomValues(a){a[0]=calls++ === 0 ? 0xffffffff : 5;return a;}};
  assert.equal(randomIndex(3,source),2); assert.equal(calls,2);
  assert.equal(randomIndex(1),0);
  for(let i=0;i<100;i++) {const n=randomIndex(20,null);assert.ok(n>=0&&n<20);}
  for(const n of [0,-1,1.5,NaN,0x100000001]) assert.throws(()=>randomIndex(n));
});
test('1000 full consecutive rounds across every count: one imposter, same word, no hints, resets', () => {
  let s=initialState(), previous=null;
  const selections=Array(20).fill(0);
  for(let round=0;round<1000;round++) {
    const count=3+(round%18);
    if(s.phase==='ANSWER') s=transition(s,{type:'SETUP'});
    s=transition(s,{type:'COUNT',count});
    s=transition(s,{type:'START'});
    assert.equal(s.phase,'PASS_PHONE');assert.equal(s.player,0);assert.equal(s.count,count);
    assert.notEqual(s.round.pair.word,previous);previous=s.round.pair.word;
    let imposters=0;const words=[];
    for(let p=0;p<count;p++) {
      assert.equal(roleFor(s),null);
      assert.equal(s.player,p);
      s=transition(s,{type:'REVEAL'});
      const role=roleFor(s);
      assert.ok(!('hint' in role));
      if(role.imposter) {imposters++;assert.ok(!('word' in role));selections[p]++;}
      else words.push(role.word);
      s=transition(s,{type:'HIDE'});
      assert.equal(s.phase,p===count-1?'DISCUSSION':'PASS_PHONE');
      assert.equal(roleFor(s),null);
    }
    assert.equal(imposters,1);assert.equal(words.length,count-1);
    assert.ok(words.every(word=>word===s.round.pair.word));
    assert.ok(WORDS.includes(s.round.pair));
    const roundData=s.round;
    s=transition(s,{type:'ANSWER'});assert.equal(s.phase,'ANSWER');assert.equal(s.round,roundData);
  }
  assert.equal(selections.reduce((a,b)=>a+b,0),1000);
});
test('NEW_ROUND repeatedly preserves count and starts hidden at player 1',()=>{
  let s=initialState(20),last=null;
  for(let i=0;i<150;i++) {
    s=transition(s,{type:i?'NEW_ROUND':'START'});
    assert.equal(s.phase,'PASS_PHONE');assert.equal(s.count,20);assert.equal(s.player,0);
    assert.equal(roleFor(s),null);assert.notEqual(s.round.pair.word,last);last=s.round.pair.word;
    for(let p=0;p<20;p++){s=transition(s,{type:'REVEAL'});s=transition(s,{type:'HIDE'});}
    s=transition(s,{type:'ANSWER'});
  }
});
test('same imposter may be selected in consecutive rounds and privacy hides current role',()=>{
  let s=transition(initialState(),{type:'START'},()=>0);
  assert.equal(s.round.imposter,0);
  s=transition(s,{type:'REVEAL'});s=transition(s,{type:'PRIVACY'});
  assert.equal(s.phase,'PASS_PHONE');assert.equal(s.player,0);assert.equal(roleFor(s),null);
  for(let p=0;p<4;p++){s=transition(s,{type:'REVEAL'});s=transition(s,{type:'HIDE'});}
  s=transition(s,{type:'ANSWER'});s=transition(s,{type:'NEW_ROUND'},()=>0);
  assert.equal(s.round.imposter,0);
});
