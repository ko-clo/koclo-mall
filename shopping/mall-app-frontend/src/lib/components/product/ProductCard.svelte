<script lang="ts">
	import type { Product } from '$lib/data/products';
	import { formatPrice } from '$lib/data/products';

	interface Props {
		product: Product;
	}

	let { product }: Props = $props();
</script>

<a href="/products/{product.slug}" class="product-card block group">
	<div class="relative overflow-hidden rounded-lg bg-gray-100">
		<img
			src={product.thumbnail_url}
			alt={product.name}
			class="product-card-image"
			loading="lazy"
		/>
		<div class="product-card-overlay"></div>

		{#if product.is_sold_out}
			<div class="absolute inset-0 bg-black/50 flex items-center justify-center">
				<span class="text-white font-semibold text-lg">SOLD OUT</span>
			</div>
		{/if}

		<div class="absolute top-2 left-2 flex flex-wrap gap-1">
			{#if product.is_new}
				<span class="badge badge-new">NEW</span>
			{/if}
			{#if product.discount_rate > 0}
				<span class="badge badge-sale">{product.discount_rate}%</span>
			{/if}
		</div>
	</div>

	<div class="mt-3 space-y-1">
		<p class="text-xs text-gray-500">{product.category.name}</p>
		<h3 class="text-sm font-medium text-gray-900 line-clamp-2 group-hover:text-accent transition-colors">
			{product.name}
		</h3>
		<div class="flex items-center gap-2">
			{#if product.discount_rate > 0}
				<span class="price-discount">{product.discount_rate}%</span>
			{/if}
			<span class="price-current">{formatPrice(product.display_price)}</span>
		</div>
		{#if product.discount_rate > 0}
			<p class="price-original">{formatPrice(product.original_price)}</p>
		{/if}
	</div>
</a>
