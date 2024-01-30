<script lang="ts">
	import { getContext } from 'svelte';
	import { type Select, melt } from '@melt-ui/svelte';

	const {
		elements: { label }
	} = getContext<Select>('select');
</script>

<label use:melt={$label} class="mb-1 block text-navy-400">
	<slot />
</label>
