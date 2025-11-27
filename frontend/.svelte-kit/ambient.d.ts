
// this file is generated — do not edit it


/// <reference types="@sveltejs/kit" />

/**
 * Environment variables [loaded by Vite](https://vitejs.dev/guide/env-and-mode.html#env-files) from `.env` files and `process.env`. Like [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), this module cannot be imported into client-side code. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured).
 * 
 * _Unlike_ [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), the values exported from this module are statically injected into your bundle at build time, enabling optimisations like dead code elimination.
 * 
 * ```ts
 * import { API_KEY } from '$env/static/private';
 * ```
 * 
 * Note that all environment variables referenced in your code should be declared (for example in an `.env` file), even if they don't have a value until the app is deployed:
 * 
 * ```
 * MY_FEATURE_FLAG=""
 * ```
 * 
 * You can override `.env` values from the command line like so:
 * 
 * ```sh
 * MY_FEATURE_FLAG="enabled" npm run dev
 * ```
 */
declare module '$env/static/private' {
	export const NVM_INC: string;
	export const POSTGRES_PORT: string;
	export const NoDefaultCurrentDirectoryInExePath: string;
	export const CLAUDE_CODE_ENTRYPOINT: string;
	export const NODE: string;
	export const JEDITERM_SOURCE_ARGS: string;
	export const INIT_CWD: string;
	export const NVM_CD_FLAGS: string;
	export const POSTGRES_DB: string;
	export const HOST: string;
	export const SHELL: string;
	export const TERM: string;
	export const CORS_ORIGINS: string;
	export const HOMEBREW_REPOSITORY: string;
	export const TMPDIR: string;
	export const npm_config_global_prefix: string;
	export const COLOR: string;
	export const FLASK_ENV: string;
	export const TERM_SESSION_ID: string;
	export const npm_config_noproxy: string;
	export const npm_config_local_prefix: string;
	export const ENABLE_IDE_INTEGRATION: string;
	export const GIT_EDITOR: string;
	export const PROCESS_LAUNCHED_BY_Q: string;
	export const NVM_DIR: string;
	export const USER: string;
	export const COMMAND_MODE: string;
	export const npm_config_globalconfig: string;
	export const SSH_AUTH_SOCK: string;
	export const CLAUDE_CODE_SSE_PORT: string;
	export const __CF_USER_TEXT_ENCODING: string;
	export const npm_execpath: string;
	export const VIRTUAL_ENV: string;
	export const POSTGRES_PASSWORD: string;
	export const NVM_DEFAULT: string;
	export const PATH: string;
	export const TERMINAL_EMULATOR: string;
	export const npm_package_json: string;
	export const _: string;
	export const IJ_RESTARTER_LOG: string;
	export const npm_config_userconfig: string;
	export const npm_config_init_module: string;
	export const SECRET_KEY: string;
	export const __CFBundleIdentifier: string;
	export const npm_command: string;
	export const PWD: string;
	export const JAVA_HOME: string;
	export const npm_lifecycle_event: string;
	export const EDITOR: string;
	export const OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE: string;
	export const npm_package_name: string;
	export const LANG: string;
	export const npm_config_npm_version: string;
	export const XPC_FLAGS: string;
	export const POSTGRES_USER: string;
	export const npm_config_node_gyp: string;
	export const HTTPS_PROXY: string;
	export const npm_package_version: string;
	export const XPC_SERVICE_NAME: string;
	export const LOG_LEVEL: string;
	export const M2_HOME: string;
	export const SHLVL: string;
	export const HOME: string;
	export const HOMEBREW_PREFIX: string;
	export const HTTP_PROXY: string;
	export const PROCESS_LAUNCHED_BY_CW: string;
	export const npm_config_cache: string;
	export const LOGNAME: string;
	export const npm_lifecycle_script: string;
	export const LC_CTYPE: string;
	export const COREPACK_ENABLE_AUTO_PIN: string;
	export const NVM_BIN: string;
	export const npm_config_user_agent: string;
	export const JEDITERM_SOURCE: string;
	export const PORT: string;
	export const INFOPATH: string;
	export const HOMEBREW_CELLAR: string;
	export const OSLogRateLimit: string;
	export const CLAUDECODE: string;
	export const DATABASE_URL: string;
	export const POSTGRES_HOST: string;
	export const VIRTUAL_ENV_PROMPT: string;
	export const npm_node_execpath: string;
	export const npm_config_prefix: string;
	export const FIG_TERM: string;
	export const NODE_ENV: string;
}

/**
 * Similar to [`$env/static/private`](https://svelte.dev/docs/kit/$env-static-private), except that it only includes environment variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Values are replaced statically at build time.
 * 
 * ```ts
 * import { PUBLIC_BASE_URL } from '$env/static/public';
 * ```
 */
declare module '$env/static/public' {
	
}

/**
 * This module provides access to runtime environment variables, as defined by the platform you're running on. For example if you're using [`adapter-node`](https://github.com/sveltejs/kit/tree/main/packages/adapter-node) (or running [`vite preview`](https://svelte.dev/docs/kit/cli)), this is equivalent to `process.env`. This module only includes variables that _do not_ begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) _and do_ start with [`config.kit.env.privatePrefix`](https://svelte.dev/docs/kit/configuration#env) (if configured).
 * 
 * This module cannot be imported into client-side code.
 * 
 * ```ts
 * import { env } from '$env/dynamic/private';
 * console.log(env.DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 * 
 * > [!NOTE] In `dev`, `$env/dynamic` always includes environment variables from `.env`. In `prod`, this behavior will depend on your adapter.
 */
declare module '$env/dynamic/private' {
	export const env: {
		NVM_INC: string;
		POSTGRES_PORT: string;
		NoDefaultCurrentDirectoryInExePath: string;
		CLAUDE_CODE_ENTRYPOINT: string;
		NODE: string;
		JEDITERM_SOURCE_ARGS: string;
		INIT_CWD: string;
		NVM_CD_FLAGS: string;
		POSTGRES_DB: string;
		HOST: string;
		SHELL: string;
		TERM: string;
		CORS_ORIGINS: string;
		HOMEBREW_REPOSITORY: string;
		TMPDIR: string;
		npm_config_global_prefix: string;
		COLOR: string;
		FLASK_ENV: string;
		TERM_SESSION_ID: string;
		npm_config_noproxy: string;
		npm_config_local_prefix: string;
		ENABLE_IDE_INTEGRATION: string;
		GIT_EDITOR: string;
		PROCESS_LAUNCHED_BY_Q: string;
		NVM_DIR: string;
		USER: string;
		COMMAND_MODE: string;
		npm_config_globalconfig: string;
		SSH_AUTH_SOCK: string;
		CLAUDE_CODE_SSE_PORT: string;
		__CF_USER_TEXT_ENCODING: string;
		npm_execpath: string;
		VIRTUAL_ENV: string;
		POSTGRES_PASSWORD: string;
		NVM_DEFAULT: string;
		PATH: string;
		TERMINAL_EMULATOR: string;
		npm_package_json: string;
		_: string;
		IJ_RESTARTER_LOG: string;
		npm_config_userconfig: string;
		npm_config_init_module: string;
		SECRET_KEY: string;
		__CFBundleIdentifier: string;
		npm_command: string;
		PWD: string;
		JAVA_HOME: string;
		npm_lifecycle_event: string;
		EDITOR: string;
		OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE: string;
		npm_package_name: string;
		LANG: string;
		npm_config_npm_version: string;
		XPC_FLAGS: string;
		POSTGRES_USER: string;
		npm_config_node_gyp: string;
		HTTPS_PROXY: string;
		npm_package_version: string;
		XPC_SERVICE_NAME: string;
		LOG_LEVEL: string;
		M2_HOME: string;
		SHLVL: string;
		HOME: string;
		HOMEBREW_PREFIX: string;
		HTTP_PROXY: string;
		PROCESS_LAUNCHED_BY_CW: string;
		npm_config_cache: string;
		LOGNAME: string;
		npm_lifecycle_script: string;
		LC_CTYPE: string;
		COREPACK_ENABLE_AUTO_PIN: string;
		NVM_BIN: string;
		npm_config_user_agent: string;
		JEDITERM_SOURCE: string;
		PORT: string;
		INFOPATH: string;
		HOMEBREW_CELLAR: string;
		OSLogRateLimit: string;
		CLAUDECODE: string;
		DATABASE_URL: string;
		POSTGRES_HOST: string;
		VIRTUAL_ENV_PROMPT: string;
		npm_node_execpath: string;
		npm_config_prefix: string;
		FIG_TERM: string;
		NODE_ENV: string;
		[key: `PUBLIC_${string}`]: undefined;
		[key: `${string}`]: string | undefined;
	}
}

/**
 * Similar to [`$env/dynamic/private`](https://svelte.dev/docs/kit/$env-dynamic-private), but only includes variables that begin with [`config.kit.env.publicPrefix`](https://svelte.dev/docs/kit/configuration#env) (which defaults to `PUBLIC_`), and can therefore safely be exposed to client-side code.
 * 
 * Note that public dynamic environment variables must all be sent from the server to the client, causing larger network requests — when possible, use `$env/static/public` instead.
 * 
 * ```ts
 * import { env } from '$env/dynamic/public';
 * console.log(env.PUBLIC_DEPLOYMENT_SPECIFIC_VARIABLE);
 * ```
 */
declare module '$env/dynamic/public' {
	export const env: {
		[key: `PUBLIC_${string}`]: string | undefined;
	}
}
