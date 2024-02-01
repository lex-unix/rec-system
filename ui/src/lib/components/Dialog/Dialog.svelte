<script context="module" lang="ts">
	export type Size = 'sm' | 'md' | 'lg';
</script>

<script lang="ts">
	import { createEventDispatcher, setContext } from 'svelte';
	import { createDialog } from '@melt-ui/svelte';
	import type { ChangeFn } from '@melt-ui/svelte/internal/helpers';

	export let size: Size = 'md';

	export function show() {
		$open = true;
	}

	export function dismiss() {
		$open = false;
	}

	const dispatch = createEventDispatcher();

	const onOpenChange: ChangeFn<boolean> = ({ next, curr }) => {
		if (curr === true) {
			dispatch('close');
		} else {
			dispatch('open');
		}
		return next;
	};

	const ctx = createDialog({
		forceVisible: true,
		closeOnOutsideClick: true,
		onOpenChange
	});
	setContext('dialog', ctx);
	setContext('size', size);

	const {
		states: { open }
	} = ctx;
</script>

<slot />
