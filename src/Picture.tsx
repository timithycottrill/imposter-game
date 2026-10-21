import { PICTURE_INDEX, ATLAS_COLUMNS, ATLAS_ROWS } from './picture-index';
export const WORD_ART = `${import.meta.env.BASE_URL}art/words.webp`;
export const IMPOSTER_ART = `${import.meta.env.BASE_URL}art/imposter.webp`;
/** A different, stable illustrated scene for each player's private role. */
export function Picture({ word, variant, imposter = false }: { word?: string; variant: number; imposter?: boolean }) {
  const hue = imposter ? 350 + variant % 14 : (variant * 137 + 150) % 360;
  const index = word ? PICTURE_INDEX[word] : undefined;
  if (!imposter && index === undefined) throw new Error('No illustration for this secret word');
  const col = (index ?? 0) % ATLAS_COLUMNS;
  const row = Math.floor((index ?? 0) / ATLAS_COLUMNS);
  const tilt = (variant % 7 - 3) * 3;
  const shift = (variant % 5 - 2) * 8;
  const mirror = variant % 2 ? -1 : 1;
  return <svg className="role-picture" viewBox="0 0 320 224" role="img"
    aria-label={imposter ? 'A mischievous red imposter with a sly grin' : `Illustration of ${word}`}
    data-picture={imposter ? 'imposter' : 'word'} data-variant={variant} data-subject={imposter ? 'IMPOSTER' : word}>
    <ellipse cx="160" cy="112" rx="131" ry="102" fill={`hsl(${hue} 55% 17%)`} />
    <circle cx={72 + variant % 4 * 18} cy="48" r={18 + variant % 3 * 7} fill={`hsl(${hue} 70% 31%)`} />
    <path d={variant % 2 ? 'M36 162Q160 111 284 162' : 'M36 162Q160 198 284 162'} fill="none" stroke={`hsl(${hue} 65% 35%)`} strokeWidth="3" />
    <ellipse cx={160 + shift} cy="195" rx="68" ry="9" fill="#000" opacity=".24" />
    <g transform={`translate(${160 + shift} 112) rotate(${tilt}) scale(${mirror} 1) translate(-160 -112)`}>
      {imposter ? <image href={IMPOSTER_ART} x="49" y="0" width="222" height="220" /> :
        <svg x={variant % 3 === 0 ? 66 : 72} y={variant % 3 === 0 ? 10 : 18} width={variant % 3 === 0 ? 188 : 176} height="176"
          viewBox={`${col * 128} ${row * 128} 128 128`} overflow="hidden">
          <image href={WORD_ART} width={ATLAS_COLUMNS * 128} height={ATLAS_ROWS * 128} />
        </svg>}
    </g>
    <g fill={`hsl(${hue} 85% 75%)`}>
      <path d={`M${266 - variant % 3 * 9} 49l3 9 9 3-9 3-3 9-3-9-9-3 9-3Z`} />
      <circle cx={43 + variant % 4 * 8} cy="120" r="4" />
      <circle cx="269" cy={140 + variant % 4 * 9} r="5" />
    </g>
  </svg>;
}
