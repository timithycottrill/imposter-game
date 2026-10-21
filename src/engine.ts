import { WORDS } from './words';
export { WORDS };

export type Phase = 'SETUP'|'PASS_PHONE'|'REVEAL_ROLE'|'DISCUSSION'|'ANSWER';
export type Round = { pair: (typeof WORDS)[number]; imposter: number };
export type State = { phase: Phase; count: number; player: number; round: Round | null; previousWord: string | null };
export type GameEvent = { type: 'COUNT'; count: number } | { type: 'START'|'NEW_ROUND'|'REVEAL'|'HIDE'|'ANSWER'|'SETUP'|'PRIVACY' };
export type Picker = (max: number) => number;
/** Uniform integer in [0, max). Rejection sampling avoids modulo bias. */
export function randomIndex(max: number, source: Pick<Crypto, "getRandomValues"> | null = globalThis.crypto) {
  if (!Number.isSafeInteger(max) || max < 1 || max > 0x100000000) throw new RangeError('Invalid random bound');
  if (source?.getRandomValues) {
    const limit = Math.floor(0x100000000 / max) * max;
    const values = new Uint32Array(1);
    do { source.getRandomValues(values); } while (values[0] >= limit);
    return values[0] % max;
  }
  // Safe non-cryptographic fallback for older WebViews; no security claims.
  return Math.floor(Math.random() * max);
}
export function validCount(value: unknown): value is number {
  return Number.isInteger(value) && typeof value === "number" && value >= 3 && value <= 20;
}
export function initialState(count: unknown = 4): State {
  return { phase: 'SETUP', count: validCount(count) ? count : 4, player: 0, round: null, previousWord: null };
}
export function generateRound(count: number, previousWord: string | null = null, pick: Picker = randomIndex): Round {
  if (!validCount(count)) throw new RangeError('Use 3–20 players');
  const candidates = WORDS.filter(entry => entry.word !== previousWord);
  const pair = candidates[pick(candidates.length)];
  return { pair, imposter: pick(count) };
}
/** Only public information for the current private screen. No hint is returned. */
export function roleFor(state: State) {
  if (state.phase !== 'REVEAL_ROLE' || !state.round) return null;
  return state.player === state.round.imposter
    ? { imposter: true }
    : { imposter: false, word: state.round.pair.word };
}
/** Central finite-state machine. Invalid/out-of-phase events are harmless. */
export function transition(state: State, event: GameEvent, pick: Picker = randomIndex): State {
  switch (event.type) {
    case 'COUNT':
      return state.phase === 'SETUP' && validCount(event.count) ? { ...state, count: event.count } : state;
    case 'START':
    case 'NEW_ROUND': {
      if (event.type === 'START' ? state.phase !== 'SETUP' : state.phase !== 'ANSWER') return state;
      const round = generateRound(state.count, state.previousWord, pick);
      return { ...state, phase: 'PASS_PHONE', player: 0, round, previousWord: round.pair.word };
    }
    case 'REVEAL': return state.phase === 'PASS_PHONE' ? { ...state, phase: 'REVEAL_ROLE' } : state;
    case 'HIDE': return state.phase === 'REVEAL_ROLE' ? {
      ...state, phase: state.player === state.count - 1 ? 'DISCUSSION' : 'PASS_PHONE',
      player: state.player === state.count - 1 ? state.player : state.player + 1,
    } : state;
    case 'ANSWER': return state.phase === 'DISCUSSION' ? { ...state, phase: 'ANSWER' } : state;
    case 'SETUP': return state.phase === 'ANSWER' ? { ...initialState(state.count), previousWord: state.previousWord } : state;
    case 'PRIVACY': return state.phase === 'REVEAL_ROLE' ? { ...state, phase: 'PASS_PHONE' } : state;
    default: return state;
  }
}
