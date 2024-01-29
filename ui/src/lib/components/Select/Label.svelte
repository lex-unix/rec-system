<script lang="ts">
	import { getContext } from 'svelte';
	import { type Select, melt } from '@melt-ui/svelte';

	const {
		elements: { label }
	} = getContext<Select>('select');
</script>

<label use:melt={$label} class="text-navy-400 mb-1 block">
	<slot />
</label>
