<script lang="ts">
	import { getContext } from 'svelte';
	import { type Select, melt } from '@melt-ui/svelte';
	import { ChevronDown } from 'lucide-svelte';
	import { cn } from '$lib';

	export let label: string;
	let className = '';
	export { className as class };

	const {
		elements: { trigger },
		states: { selectedLabel }
	} = getContext<Select>('select');
</script>

<button
	use:melt={$trigger}
	aria-label="Issue type"
	class={cn(
		'flex h-10 w-[220px] items-center justify-between rounded-md border border-navy-200/10 bg-navy-800 px-3 py-2 opacity-70 transition-opacity hover:opacity-100 focus:opacity-100 focus:outline-none focus-visible:opacity-100 focus-visible:ring-2 focus-visible:ring-[#479EFA] aria-expanded:opacity-60 aria-expanded:ring-transparent',
		className
	)}
>
	{$selectedLabel || label}
	<ChevronDown class="h-5 w-5" />
</button>
