// @ts-nocheck
import type { LayoutLoad } from './$types';
import { env } from '$env/dynamic/public';

export const prerender = false;

export const load = async () => {
  const apiBaseUrl = env.PUBLIC_API_BASE_URL || 'http://localhost:8000';
  return {
    apiBaseUrl
  };
};
;null as any as LayoutLoad;