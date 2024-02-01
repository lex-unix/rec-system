<script lang="ts">
	import { SearchIcon } from 'lucide-svelte';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	function search(
		e: Event & { currentTarget: EventTarget & HTMLInputElement }
	) {
		const input = e.target as HTMLInputElement;
		dispatch('search', { search: input.value });
	}
</script>

<div
	class="border-navy-200/10 focus-within:border-navy-200/25 relative h-10 w-full rounded-md border"
>
	<div class="absolute left-3 top-1/2 -translate-y-1/2">
		<SearchIcon class="text-navy-400 square-4" />
	</div>
	<input
		type="search"
		class="placeholder:text-navy-400 h-full w-full bg-transparent pl-10 focus:outline-none"
		placeholder="Search..."
		on:input={search}
	/>
</div>
