<script lang="ts">
  import { onMount } from 'svelte';

  export let duration: number = 200;

  let wrapper: HTMLDivElement;
  let container: HTMLDivElement;

  onMount(() => {
    let animationFrame: number;
    const observer = new ResizeObserver(() => {
      animationFrame = requestAnimationFrame(() => {
        wrapper.style.setProperty('--height', `${container.offsetHeight}px`);
      });
    });
    observer.observe(container);

    return () => {
      cancelAnimationFrame(animationFrame);
      observer.disconnect();
    };
  });
</script>

<div bind:this={wrapper} class="wrapper" style="--duration: {duration}ms;">
  <div bind:this={container}>
    <slot />
  </div>
</div>

<style lang="postcss">
  .wrapper {
    height: var(--height);
    transition-property: height;
    transition-timing-function: ease;
    transition-duration: var(--duration);
    overflow: auto;
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .wrapper::-webkit-scrollbar {
    display: none;
  }
</style>
