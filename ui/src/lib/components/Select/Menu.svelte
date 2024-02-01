<script lang="ts">
	import { getContext } from 'svelte';
	import { type Select, melt } from '@melt-ui/svelte';
	import { cn } from '$lib';

	let className = '';
	export { className as class };

	const {
		elements: { menu },
		states: { open }
	} = getContext<Select>('select');
</script>

{#if $open}
	<div
		use:melt={$menu}
		class={cn(
			'z-10 flex !max-h-[220px] flex-col gap-0.5 overflow-y-auto rounded-lg border border-navy-200/10 bg-navy-800 p-1 shadow-lg focus:outline-none',
			className
		)}
	>
		<slot />
	</div>
{/if}
