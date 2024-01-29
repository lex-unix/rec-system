<script lang="ts">
	import type { HTMLInputTypeAttribute } from 'svelte/elements';

	export let value: string = '';
	export let placeholder: string | undefined = undefined;
	export let required: boolean = false;
	export let id: string;
	export let name: string;
	export let type: HTMLInputTypeAttribute = 'text';

	function change(
		e: Event & { currentTarget: EventTarget & HTMLInputElement }
	) {
		value = e.currentTarget.value;
	}
</script>

<input
	{id}
	{name}
	{type}
	{value}
	{required}
	{placeholder}
	class="border-navy-200/10 bg-navy-800 text-navy-50 placeholder:text-navy-500 hover:border-navy-200/25 focus:border-navy-200/25 focus:ring-navy-600 h-10 w-full max-w-[420px] rounded-md border px-3 py-2 focus:outline-none focus:ring-2"
	on:input={change}
/>
