<script context="module" lang="ts">
	export type Size = 'sm' | 'md' | 'lg';
</script>

<script lang="ts">
	import { setContext } from 'svelte';
	import { createDialog } from '@melt-ui/svelte';

	export let size: Size = 'md';

	export function show() {
		$open = true;
	}

	export function dismiss() {
		$open = false;
	}

	const ctx = createDialog({
		forceVisible: true,
		closeOnOutsideClick: true
	});
	setContext('dialog', ctx);
	setContext('size', size);

	const {
		states: { open }
	} = ctx;
</script>

<slot />
