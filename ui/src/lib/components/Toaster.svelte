<script lang="ts" context="module">
  export type ToastData = {
    title: string;
    description: string;
  };

  const {
    elements: { content, title, description, close },
    helpers,
    states: { toasts },
    actions: { portal }
  } = createToaster<ToastData>();

  export const addToast = helpers.addToast;
</script>

<script lang="ts">
  import { createToaster, melt } from '@melt-ui/svelte';
  import { flip } from 'svelte/animate';
  import { fly } from 'svelte/transition';
  import { X } from 'lucide-svelte';
</script>

<div
  class="fixed bottom-0 right-0 z-[1000] m-4 flex flex-col items-end gap-2"
  use:portal
>
  {#each $toasts as { id, data } (id)}
    <div
      use:melt={$content(id)}
      animate:flip={{ duration: 500 }}
      in:fly={{ duration: 150, x: '100%' }}
      out:fly={{ duration: 150, x: '100%' }}
      class="rounded-lg border border-navy-200/10 bg-navy-800 text-white shadow-md"
    >
      <div
        class="relative flex w-[24rem] max-w-[calc(100vw-2rem)] items-center justify-between gap-4 p-5"
      >
        <div>
          <h3
            use:melt={$title(id)}
            class="flex items-center gap-2 font-semibold"
          >
            {data.title}
          </h3>
          <div use:melt={$description(id)} class="text-navy-400">
            {data.description}
          </div>
        </div>
        <button
          use:melt={$close(id)}
          class="absolute right-4 top-4 grid h-6 w-6 place-items-center rounded-full hover:bg-navy-100/10"
        >
          <X class="h-4 w-4" />
        </button>
      </div>
    </div>
  {/each}
</div>
