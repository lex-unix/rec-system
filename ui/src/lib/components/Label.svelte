<script lang="ts">
	export let htmlFor: string;
</script>

<label for={htmlFor} class="text-navy-400 mb-1 block">
	<slot />
</label>
