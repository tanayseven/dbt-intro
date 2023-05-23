{% call dbt_unit_testing.test('customers', 'should sum order values to calculate customer_lifetime_value') %}

  {% call dbt_unit_testing.mock_source ('shop', 'stg_customers') %}
    customer_id | first_name | last_name
    1           | ''         | ''
  {% endcall %}

  {% call dbt_unit_testing.mock_source ('shop', 'stg_orders') %}
    order_id | customer_id | order_date
    1        | 1           | null
    2        | 1           | null
  {% endcall %}

  {% call dbt_unit_testing.mock_source ('shop', 'stg_payments') %}
    order_id | amount
    1        | 10
    2        | 10
  {% endcall %}

  {% call dbt_unit_testing.expect() %}
    customer_id | customer_lifetime_value
    1           | 20
  {% endcall %}
{% endcall %}
