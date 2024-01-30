<script lang="ts">
	export let id: string;
	export let name: string;
	export let value: string;
	export let required: boolean = false;
</script>

<textarea
	{id}
	{name}
	{required}
	class="max-h-[400px] min-h-[100px] w-full max-w-[520px] resize-y rounded-md border border-navy-200/10 bg-navy-800 px-3 py-2 hover:border-navy-200/25 focus:border-navy-200/25 focus:outline-none focus:ring-2 focus:ring-navy-600"
	bind:value
/>
