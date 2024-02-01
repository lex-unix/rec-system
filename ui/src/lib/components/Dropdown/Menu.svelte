<script lang="ts">
	import { getContext } from 'svelte';
	import { type DropdownMenu, melt } from '@melt-ui/svelte';
	import { flyAndScale } from '$transitions';

	const {
		elements: { menu },
		states: { open }
	} = getContext<DropdownMenu>('dropdown');
</script>

{#if $open}
	<div
		use:melt={$menu}
		transition:flyAndScale={{ duration: 100, y: 3, start: 0.97 }}
		class="z-10 flex min-w-[220px] flex-col rounded-md border border-navy-200/10 bg-navy-900 p-1 shadow-lg focus:outline-none"
	>
		<slot />
	</div>
{/if}
