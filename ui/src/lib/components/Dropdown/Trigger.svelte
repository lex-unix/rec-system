<script lang="ts">
	import { getContext } from 'svelte';
	import { type DropdownMenu, melt } from '@melt-ui/svelte';
	import { cn } from '$lib';

	let className: string = '';
	export { className as class };

	const {
		elements: { trigger }
	} = getContext<DropdownMenu>('dropdown');
</script>

<button
	use:melt={$trigger}
	class={cn(
		'flex items-center gap-2 rounded-md border border-navy-200/10 bg-navy-800 px-4 py-3 font-medium opacity-70 transition hover:opacity-100 focus:outline-none focus-visible:opacity-100 focus-visible:ring-2 focus-visible:ring-[#479EFA] data-[state=open]:opacity-40',
		className
	)}
>
	<slot name="icon" />
	<span class="leading-none">
		<slot />
	</span>
</button>
