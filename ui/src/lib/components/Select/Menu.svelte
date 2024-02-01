<script lang="ts">
	import { getContext } from 'svelte';
	import { type Select, melt } from '@melt-ui/svelte';

	const {
		elements: { menu },
		states: { open }
	} = getContext<Select>('select');
</script>

{#if $open}
	<div
		use:melt={$menu}
		class="z-10 flex !max-h-[220px] flex-col gap-0.5 overflow-y-auto rounded-lg border border-navy-200/10 bg-navy-800 p-1 shadow-lg focus:outline-none"
	>
		<slot />
	</div>
{/if}
