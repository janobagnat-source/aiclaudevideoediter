// Acceso perezoso al registro de gráficos (evita import circular MainTrack <-> GraphicsLayer)
import type React from 'react';
import {REGISTRY} from './GraphicsLayer';

export const REGISTRY_BEHIND = (): Record<string, React.FC<any>> => REGISTRY;
