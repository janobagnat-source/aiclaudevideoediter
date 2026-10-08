/**
 * Note: When using the Node.JS APIs, the config file
 * doesn't apply. Instead, pass options directly to the APIs.
 *
 * All configuration options: https://remotion.dev/docs/config
 */

import { Config } from "@remotion/cli/config";

Config.setRspack(true);
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// Nube sin GPU: SwiftShader (swangle). En una máquina con GPU usar "angle" (más rápido).
Config.setChromiumOpenGlRenderer((process.env.REMOTION_GL as 'swangle' | 'angle') || 'swangle');
Config.setConcurrency(null);
