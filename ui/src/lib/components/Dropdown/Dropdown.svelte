<script lang="ts">
	import { setContext } from 'svelte';
	import { createDropdownMenu } from '@melt-ui/svelte';

	export function show() {
		$open = true;
	}

	export function dismiss() {
		$open = false;
	}

	const ctx = createDropdownMenu({
		forceVisible: true,
		loop: false
	});
	setContext('dropdown', ctx);

	const {
		states: { open }
	} = ctx;
</script>

<slot />
