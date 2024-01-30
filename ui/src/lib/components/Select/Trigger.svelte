<script lang="ts">
	import { getContext } from 'svelte';
	import { type Select, melt } from '@melt-ui/svelte';
	import { ChevronDown } from 'lucide-svelte';

	export let label: string;

	const {
		elements: { trigger },
		states: { selectedLabel }
	} = getContext<Select>('select');
</script>

<button
	use:melt={$trigger}
	aria-label="Issue type"
	class="flex h-10 w-[220px] items-center justify-between rounded-md border border-navy-200/10 bg-navy-800 px-3 py-2 hover:border-navy-200/25 focus:outline-none focus-visible:border-navy-200/25 focus-visible:ring-2 focus-visible:ring-navy-600 aria-expanded:opacity-60 aria-expanded:ring-transparent"
>
	{$selectedLabel || label}
	<ChevronDown class="h-5 w-5" />
</button>
