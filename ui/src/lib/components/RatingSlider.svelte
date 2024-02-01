<script lang="ts">
  import { createSlider, melt } from '@melt-ui/svelte';

  export let rating: number;

  const {
    elements: { root, range, thumbs },
    states: { value }
  } = createSlider({
    defaultValue: [0.5],
    min: 0.5,
    step: 0.5,
    max: 5
  });

  $: rating = $value[0];
</script>

<div class="mb-1 flex items-center gap-4">
  <span use:melt={$root} class="relative">
    <span use:melt={$range} class="h-full w-full rounded bg-transparent" />
    <span
      use:melt={$thumbs[0]}
      class="h-full w-full bg-transparent square-6 focus:outline-none"
    />
    <div class="flex justify-between gap-2">
      <!-- eslint-disable-next-line @typescript-eslint/no-unused-vars -->
      {#each Array(5) as _, i}
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="24"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          class={`text-navy-400 ${$value[0] - i === 0.5 ? 'halficon' : $value[0] >= i + 1 ? 'fill-navy-400' : ''} square-6`}
        >
          <linearGradient id="half">
            <stop offset="50%" stop-color="#91949F" />
            <stop offset="50%" stop-color="transparent" />
          </linearGradient>
          <polygon
            points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
          />
        </svg>
      {/each}
    </div>
  </span>
</div>

<style lang="postcss">
  .halficon {
    fill: url(#half);
  }
</style>
