<script lang="ts">
	export let htmlFor: string;
</script>

<label for={htmlFor} class="mb-1 block text-navy-400">
	<slot />
</label>
