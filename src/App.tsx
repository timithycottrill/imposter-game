import { useEffect, useLayoutEffect, useReducer, useRef } from 'react';
import { initialState, transition, roleFor, type GameEvent } from './engine';

function savedCount() {
  try { return Number(localStorage.getItem('imposter-count')); } catch { return 4; }
}
export default function App() {
  const [state, dispatch] = useReducer((s: ReturnType<typeof initialState>, e: GameEvent) => transition(s, e), undefined, () => initialState(savedCount()));
  const heading = useRef<HTMLHeadingElement>(null);
  const lastAction = useRef(-Infinity);
  function send(event: GameEvent) {
    const now = performance.now();
    if (event.type !== 'COUNT') {
      if (now - lastAction.current < 240) return;
      lastAction.current = now;
    }
    dispatch(event);
  }
  useEffect(() => {
    try { localStorage.setItem('imposter-count', String(state.count)); } catch { /* Storage is optional. */ }
  }, [state.count]);
  useLayoutEffect(() => { heading.current?.focus({ preventScroll: true }); }, [state.phase, state.player]);
  useEffect(() => {
    const hide = () => { if (document.hidden) dispatch({ type: 'PRIVACY' }); };
    const leave = () => dispatch({ type: 'PRIVACY' });
    document.addEventListener('visibilitychange', hide); window.addEventListener('pagehide', leave);
    return () => { document.removeEventListener('visibilitychange', hide); window.removeEventListener('pagehide', leave); };
  }, []);
  const button = (label: string, event: GameEvent, className = 'primary') => <button type="button" className={className} onClick={e => send(event)}>{label}</button>;
  const title = (text: string) => <h1 ref={heading} tabIndex={-1}>{text}</h1>;
  const label = (text: string) => <p className="label">{text}</p>;
  const value = (text: string) => <p className="value">{text}</p>;
  const help = (text: string) => <p className="help">{text}</p>;
  let content, footer;
  switch (state.phase) {
    case 'SETUP':
      content = <>{title('IMPOSTER')}{label('NUMBER OF PLAYERS')}<div className="counter">
        <button type="button" className="step" aria-label="Decrease number of players" disabled={state.count === 3} onClick={() => send({ type: 'COUNT', count: state.count - 1 })}>−</button>
        <output aria-live="polite" aria-label={`Number of players: ${state.count}`}>{state.count}</output>
        <button type="button" className="step" aria-label="Increase number of players" disabled={state.count === 20} onClick={() => send({ type: 'COUNT', count: state.count + 1 })}>+</button>
      </div></>;
      footer = button('START ROUND', { type: 'START' }); break;
    case 'PASS_PHONE':
      content = <>{title(`PLAYER ${state.player + 1}`)}{help(`Pass the phone to Player ${state.player + 1}.`)}{help('Make sure nobody else is looking.')}</>;
      footer = button('REVEAL', { type: 'REVEAL' }); break;
    case 'REVEAL_ROLE': {
      const role = roleFor(state)!;
      content = <>{title(`PLAYER ${state.player + 1}`)}{role.imposter ? <>{value('IMPOSTER')}{help('You do not know the secret word.')}</> : <>{label('SECRET WORD')}{value(role.word!)}</>}</>;
      footer = button(state.player === state.count - 1 ? 'FIND THE IMPOSTER' : 'HIDE & NEXT PLAYER', { type: 'HIDE' }); break;
    }
    case 'DISCUSSION':
      content = <>{title('FIND THE IMPOSTER')}{label('ONE-WORD HINT')}{value(state.round!.pair.hint)}{help('Take turns describing the word.')}{help('Find the imposter.')}</>;
      footer = button('REVEAL ANSWER', { type: 'ANSWER' }); break;
    case 'ANSWER':
      content = <>{title('SECRET WORD')}{value(state.round!.pair.word)}{label('THE IMPOSTER')}{value(`PLAYER ${state.round!.imposter + 1}`)}</>;
      footer = <>{button('NEW ROUND', { type: 'NEW_ROUND' })}{button('Change player count', { type: 'SETUP' }, 'secondary')}</>; break;
  }
  // A keyed subtree removes all previous private content in the same commit.
  return <main data-phase={state.phase}><section className="content" key={`${state.phase}-${state.player}`}>{content}</section><footer key={`action-${state.phase}-${state.player}`}>{footer}</footer></main>;
}
