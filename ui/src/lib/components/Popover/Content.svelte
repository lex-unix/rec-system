<script lang="ts">
	import { getContext } from 'svelte';
	import { type Popover, melt } from '@melt-ui/svelte';
	import { flyAndScale } from '$transitions';
	import { cn } from '$lib';

	let className = '';
	export { className as class };

	const {
		elements: { content },
		states: { open }
	} = getContext<Popover>('popover');
</script>

{#if $open}
	<div
		use:melt={$content}
		transition:flyAndScale={{ duration: 100, y: 3, start: 0.97 }}
		class={cn(
			'border-navy-200/10 bg-navy-800 z-20 w-fit max-w-[500px] rounded-lg border p-5 shadow-xl focus:outline-none',
			className
		)}
	>
		<slot />
	</div>
{/if}
