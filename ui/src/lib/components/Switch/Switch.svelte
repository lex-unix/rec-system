<script lang="ts">
  import { createSwitch } from '@melt-ui/svelte';
  import { setContext } from 'svelte';
  import type { Writable } from 'svelte/store';

  export let enabled: Writable<boolean>;
  export let id: string = 'switch-button';

  const ctx = createSwitch({ defaultChecked: $enabled });

  setContext('switch', ctx);
  setContext('id', id);

  const {
    states: { checked }
  } = ctx;

  $: $enabled = $checked;
</script>

<slot />
