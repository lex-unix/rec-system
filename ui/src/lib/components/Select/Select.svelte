<script lang="ts">
  import { setContext } from 'svelte';
  import { createSelect } from '@melt-ui/svelte';

  export let selected: string;

  const ctx = createSelect<string>({
    loop: false,
    forceVisible: true,
    positioning: { placement: 'bottom', fitViewport: true, sameWidth: true }
  });

  setContext('select', ctx);

  const {
    states: { selected: selectedStore }
  } = ctx;

  $: selected = $selectedStore?.value || '';
</script>

<slot />
