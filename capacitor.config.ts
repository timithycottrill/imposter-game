import type { CapacitorConfig } from '@capacitor/cli';
const config: CapacitorConfig = {
  appId: 'com.imposter.game', appName: 'IMPOSTER', webDir: 'dist',
  backgroundColor: '#000000',
  android: { backgroundColor: '#000000', allowMixedContent: false },
};
export default config;
