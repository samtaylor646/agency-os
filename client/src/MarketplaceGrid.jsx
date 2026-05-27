import React from 'react';
import { EntityCard } from './EntityCard';

export const MarketplaceGrid = ({ items, onEntityClick }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {items.map((item) => (
        <EntityCard key={item.id} entity={item} onClick={() => onEntityClick(item)} />
      ))}
    </div>
  );
};
