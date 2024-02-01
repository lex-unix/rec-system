<script lang="ts">
	let htmlFor: string;
	export { htmlFor as for };
</script>

<label for={htmlFor} class="text-navy-400 mb-1 block">
	<slot />
</label>
