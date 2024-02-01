<script lang="ts">
  let htmlFor: string;
  export { htmlFor as for };
</script>

<label for={htmlFor} class="mb-1 block text-navy-400">
  <slot />
</label>
