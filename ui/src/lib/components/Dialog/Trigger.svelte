<script lang="ts">
	import { getContext } from 'svelte';
	import { type Dialog, melt } from '@melt-ui/svelte';

	const {
		elements: { trigger }
	} = getContext<Dialog>('dialog');
</script>

<button
	use:melt={$trigger}
	class="flex items-center gap-2 rounded-md border border-navy-200/10 bg-navy-800 px-4 py-3 font-semibold focus:outline-none"
>
	<slot name="icon" />
	<span class="leading-none">
		<slot />
	</span>
</button>
