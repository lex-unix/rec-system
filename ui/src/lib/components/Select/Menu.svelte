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
		class="border-navy-200/10 bg-navy-800 z-10 flex !max-h-[220px] flex-col gap-0.5 overflow-y-auto rounded-lg border p-1 shadow-lg"
	>
		<slot />
	</div>
{/if}
