<script lang="ts">
	import { getContext } from 'svelte';
	import { type Dialog, melt } from '@melt-ui/svelte';
	import { cn } from '$lib';

	let className = '';
	export { className as class };

	const {
		elements: { trigger }
	} = getContext<Dialog>('dialog');
</script>

<button
	use:melt={$trigger}
	class={cn(
		'flex items-center gap-2 rounded-md border border-navy-200/10 bg-navy-800 bg-opacity-60 px-4 py-3 font-medium text-navy-300 hover:bg-opacity-100 hover:text-navy-50 focus:outline-none focus-visible:ring-2 focus-visible:ring-[#479EFA]',
		className
	)}
>
	<slot name="icon" />
	<span class="leading-none">
		<slot />
	</span>
</button>
