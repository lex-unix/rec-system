<script lang="ts">
	import { cn } from '$lib';
	import { type Select, melt } from '@melt-ui/svelte';
	import { getContext } from 'svelte';

	export let label: string;
	export let value: string;
	let className = '';
	export { className as class };

	const {
		elements: { option }
	} = getContext<Select>('select');
</script>

<div
	use:melt={$option({ value, label })}
	class={cn(
		'text-navy-300 data-[highlighted]:bg-navy-700 data-[selected]:bg-navy-700 data-[highlighted]:text-navy-50 data-[selected]:text-navy-50 relative cursor-pointer rounded-lg px-2 py-2 capitalize',
		className
	)}
>
	{label}
</div>
