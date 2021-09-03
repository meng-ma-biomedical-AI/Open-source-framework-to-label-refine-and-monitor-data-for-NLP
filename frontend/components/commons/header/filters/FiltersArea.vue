<template>
  <div class="filters__area">
    <div class="filters__content">
      <div class="container">
        <div class="filters__row">
          <HeaderTitle v-if="dataset.results.records" :dataset="dataset" />
        </div>
        <div class="filters__row">
          <SearchBar class="filters__searchbar" @submit="onTextQuerySearch" />
          <FiltersList
            :dataset="dataset"
            @applyFilter="onApplyFilter"
            @applyMetaFilter="onApplyMetaFilter"
            @applySortBy="onApplySortBy"
          ></FiltersList>
        </div>
        <FiltersTags
          :dataset="dataset"
          @clearFilter="onClearFilter"
          @clearMetaFilter="onClearMetaFilter"
          @clearAll="onClearAllFilters"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
export default {
  props: {
    dataset: {
      type: Object,
      default: () => ({}),
    },
  },
  data: () => ({
    sortable: {
      type: Boolean,
      default: false,
    },
    sortBy: "gold",
    sortByDir: "desc",
    sortOptions: [
      { filter: "annotated_as", text: "Annotated as", range: ["A", "Z"] },
      { filter: "predicted_as", text: "Predicted as", range: ["A", "Z"] },
      { filter: "confidence", text: "Confidence", range: ["0", "1"] },
    ],
  }),
  methods: {
    ...mapActions({
      search: "entities/datasets/search",
    }),
    onTextQuerySearch(text) {
      if (text === "") {
        text = undefined;
      }
      this.search({ dataset: this.dataset, query: { text } });
    },
    onApplyFilter({ filter, values }) {
      this.search({ dataset: this.dataset, query: { [filter]: values } });
    },
    onApplyMetaFilter({ filter, values }) {
      this.search({
        dataset: this.dataset,
        query: { metadata: { [filter]: values } },
      });
    },
    async onApplySortBy(sortList) {
      await this.search({
        dataset: this.dataset,
        sort: sortList,
      });
    },
    onClearFilter(filter, value) {
      this.onApplyFilter({
        filter,
        values: Array.isArray(this.dataset.query[filter])
          ? this.dataset.query[filter].filter((e) => e !== value)
          : undefined,
      });
    },
    onClearMetaFilter(filter, value) {
      this.onApplyMetaFilter({
        filter,
        values: this.dataset.query.metadata[filter].filter((f) => f !== value),
      });
    },
    onClearAllFilters() {
      this.search({ dataset: this.dataset, query: {} });
    },
  },
};
</script>

<style lang="scss" scoped>
.container {
  @extend %container;
  padding-top: 0;
  padding-bottom: 0;
  margin-left: 0;
  &--intro {
    padding-top: 2em;
    margin-bottom: 1.5em;
    &:after {
      border-bottom: 1px solid $line-light-color;
      content: "";
      margin-bottom: 1.5em;
      position: absolute;
      left: 0;
      right: 0;
    }
  }
}

.filters {
  &__area {
    display: block;
    top: -1em;
    left: 0;
    right: 0;
    z-index: 2;
    .fixed-header & {
      border-bottom: 1px solid $line-light-color;
    }
  }
  &__row {
    display: flex;
    align-items: center;
  }
  &__content {
    padding: 1em 0 0.5em 0;
    position: relative;
    z-index: 2;
  }
  &__searchbar {
    margin-right: 2em;
    .fixed-header & {
      transition: position 0.5s ease 2s;
      pointer-events: none;
      position: absolute;
      right: 0;
      left: 0;
      top: 0;
      height: 42px;
      margin-left: auto;
      margin-right: auto;
      padding-right: 4em;
    }
  }
  &--disabled {
    ::v-deep * {
      pointer-events: none !important;
      cursor: pointer;
    }
    ::v-deep .filters__searchbar {
      opacity: 0.4;
    }
    ::v-deep .filters--sort {
      align-items: center;
      opacity: 0.4;
    }
  }
}
</style>