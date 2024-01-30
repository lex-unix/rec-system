<script lang="ts">
	import { getContext } from 'svelte';
	import { type Popover, melt } from '@melt-ui/svelte';
	import { XIcon } from 'lucide-svelte';

	const {
		elements: { close }
	} = getContext<Popover>('popover');
</script>

<button
	use:melt={$close}
	aria-label="Close Popover"
	class="absolute inline-flex items-center justify-center rounded-full p-1.5 text-navy-400 hover:bg-navy-700 hover:text-navy-300 focus:outline-none focus:ring-2 focus:ring-navy-700"
>
	<XIcon class="square-4" />
</button>

<style lang="postcss">
	.sm {
		right: theme(spacing.3);
		top: theme(spacing.3);
	}

	.md {
		right: theme(spacing.5);
		top: theme(spacing.5);
	}

	.lg {
		right: theme(spacing.5);
		top: theme(spacing.5);
	}

	@media screen(md) {
		.sm {
			right: theme(spacing.6);
			top: theme(spacing.6);
		}
	}

	@media screen(lg) {
		.md {
			right: theme(spacing.9);
			right: theme(spacing.9);
		}

		.lg {
			right: theme(spacing.9);
			right: theme(spacing.9);
		}
	}
</style>
