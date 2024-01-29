<script lang="ts">
	import { type Select, melt } from '@melt-ui/svelte';
	import { getContext } from 'svelte';

	export let label: string;
	export let value: string;

	const {
		elements: { option }
	} = getContext<Select>('select');
</script>

<div
	use:melt={$option({ value, label })}
	class="text-navy-300 data-[highlighted]:bg-navy-700 data-[selected]:bg-navy-700 data-[highlighted]:text-navy-50 data-[selected]:text-navy-50 relative cursor-pointer rounded-lg px-2 py-2 capitalize"
>
	{label}
</div>
