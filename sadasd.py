
# Comparación de Tasa de Conversión
sns.barplot(x='conversion_rate', y='campaign_name', data=top_campaigns, palette='coolwarm', ax=axes[1])
axes[1].set_title("Tasa de Conversión de las Top Campañas", fontsize=14)
axes[1].set_xlabel("Tasa de Conversión", fontsize=12)
axes[1].set_ylabel("")

# Comparación de Presupuesto
sns.barplot(x='budget', y='campaign_name', data=top_campaigns, palette='coolwarm', ax=axes[2])
axes[2].set_title("Presupuesto de las Top Campañas", fontsize=14)
axes[2].set_xlabel("Presupuesto", fontsize=12)
axes[2].set_ylabel("")

plt.tight_layout()
plt.show()