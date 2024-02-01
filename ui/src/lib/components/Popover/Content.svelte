<script lang="ts">
	import { getContext } from 'svelte';
	import { type Popover, melt } from '@melt-ui/svelte';
	import { flyAndScale } from '$transitions';

	const {
		elements: { content },
		states: { open }
	} = getContext<Popover>('popover');
</script>

{#if $open}
	<div
		use:melt={$content}
		transition:flyAndScale={{ duration: 100, y: 3, start: 0.97 }}
		class="z-20 w-fit max-w-[500px] rounded-lg border border-navy-200/10 bg-navy-800 p-5 shadow-xl focus:outline-none"
	>
		<slot />
	</div>
{/if}
