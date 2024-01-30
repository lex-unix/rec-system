<script lang="ts">
	import { getContext } from 'svelte';
	import { type Dialog, melt } from '@melt-ui/svelte';
	import type { Size } from './Dialog.svelte';
	import { flyAndScale } from '$transitions';
	import { fade } from 'svelte/transition';

	const size = getContext<Size>('size');
	const {
		elements: { content, portalled, overlay },
		states: { open }
	} = getContext<Dialog>('dialog');
</script>

<div use:melt={$portalled}>
	{#if $open}
		<div
			use:melt={$overlay}
			transition:fade={{ duration: 150 }}
			class="fixed inset-0 z-50 bg-black/10 backdrop-blur-sm"
		/>
		<div
			class="fixed inset-0 z-50 grid w-full min-w-full place-items-center overflow-y-auto overflow-x-hidden p-2 md:p-6"
		>
			<div
				use:melt={$content}
				transition:flyAndScale={{ duration: 150, y: 8, start: 0.96 }}
				class:sm={size === 'sm'}
				class:md={size === 'md'}
				class:lg={size === 'lg'}
				class="relative rounded-lg border border-navy-200/10 bg-navy-800 p-5 shadow-xl"
			>
				<div class="pb-5">
					<div class="pb-2">
						<slot name="title" />
					</div>
					<slot name="description" />
				</div>
				<slot />
			</div>
		</div>
	{/if}
</div>

<style lang="postcss">
	.sm {
		width: 90vw;
		max-width: theme(maxWidth.md);
		padding: theme(spacing.3);
	}

	.md {
		width: 100%;
		padding: theme(spacing.5);
	}

	.lg {
		height: 100%;
		width: 100%;
		padding: theme(spacing.5);
	}

	@media screen(md) {
		.sm {
			padding: theme(spacing.6);
		}

		.lg {
			padding: theme(spacing.9);
		}
	}

	@media screen(lg) {
		.md {
			min-width: 720px;
			max-width: 800px;
			padding: theme(spacing.9);
		}
	}
</style>
