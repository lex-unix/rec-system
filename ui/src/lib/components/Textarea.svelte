<script lang="ts">
	import { cn } from '$lib';

	export let id: string;
	export let name: string;
	export let value: string;
	export let required: boolean = false;
	let className = '';
	export { className as class };
</script>

<textarea
	{id}
	{name}
	{required}
	autocomplete="off"
	spellcheck="false"
	class={cn(
		'focus:border-ring-600 border-navy-200/10 bg-navy-800 hover:border-navy-200/25 focus:ring-navy-600 max-h-[400px] min-h-[100px] w-full max-w-[520px] resize-y rounded-md border px-3 py-2 focus:outline-none focus:ring-2',
		className
	)}
	bind:value
/>
