"""
Sales Forecast Web Application
Streamlit app for predicting total sales by item_id across all shops
"""

import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Sales Forecast System",
    layout="wide"
)

# Load predictions data
@st.cache_data
def load_data():
    """Load prediction results from CSV file"""
    df = pd.read_csv('result.csv')
    return df

# Load item metadata
@st.cache_data
def load_item_info():
    """Load item information for display"""
    try:
        items_df = pd.read_csv('data/items.csv')
        return items_df
    except:
        return None

def get_sample_items(df, n=10):
    """Get sample item_ids for user selection"""
    # Get items with diverse prediction values
    item_totals = df.groupby('item_id')['item_cnt_month'].sum().reset_index()
    item_totals = item_totals.sort_values('item_cnt_month', ascending=False)
    
    # Select diverse samples: top sellers, medium, and low
    top_items = item_totals.head(3)['item_id'].tolist()
    mid_items = item_totals.iloc[len(item_totals)//2:len(item_totals)//2+4]['item_id'].tolist()
    low_items = item_totals.tail(3)['item_id'].tolist()
    
    return top_items + mid_items + low_items

def predict_sales(df, item_id):
    """
    Get total predicted sales for an item across all shops
    
    Args:
        df: Prediction dataframe
        item_id: Item ID to lookup
        
    Returns:
        dict with prediction details
    """
    # Filter by item_id
    item_predictions = df[df['item_id'] == item_id]
    
    if len(item_predictions) == 0:
        return None
    
    # Calculate total sales across all shops
    total_sales = item_predictions['item_cnt_month'].sum()
    n_shops = len(item_predictions)
    avg_per_shop = total_sales / n_shops if n_shops > 0 else 0
    
    # Get top shops for this item
    top_shops = item_predictions.nlargest(5, 'item_cnt_month')[['shop_id', 'item_cnt_month']]
    
    return {
        'total_sales': total_sales,
        'n_shops': n_shops,
        'avg_per_shop': avg_per_shop,
        'top_shops': top_shops
    }

# Main app
def main():
    st.title("Sales Forecast System")
    st.markdown("### Predict total sales for November 2015 by Item ID")
    
    # Load data
    with st.spinner("Loading prediction data..."):
        df = load_data()
        try:
            items_info = load_item_info()
        except:
            items_info = None
    
    # Sidebar with info
    with st.sidebar:
        st.header("About")
        st.markdown("""
        This system predicts the total sales quantity for a specific item across all shops in November 2015.
        
        **How to use:**
        1. Select a sample item or enter an Item ID
        2. Click 'Predict Sales'
        3. View the prediction results
        
        **Model:** LightGBM with 30+ engineered features
        """)
        
        st.markdown("---")
        st.markdown(f"**Total Items in Dataset:** {df['item_id'].nunique():,}")
        st.markdown(f"**Total Shops:** {df['shop_id'].nunique()}")
        st.markdown(f"**Total Predictions:** {len(df):,}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Input Item ID")
        
        # Get sample items and all items
        sample_items = get_sample_items(df)
        all_items = sorted(df['item_id'].unique().tolist())
        
        # Create options list with samples at top
        options = [0] + sample_items + [item for item in all_items if item not in sample_items]
        
        # Single selectbox for item selection
        item_id_input = st.selectbox(
            "Select or search for an Item ID:",
            options=options,
            format_func=lambda x: "-- Select an Item ID --" if x == 0 else f"Item ID: {x}",
            help="You can type to search or scroll to select from the list. Sample items are shown first."
        )
        
        st.markdown("**Tip:** Start typing numbers to quickly find an item ID")
        
        # Predict button
        predict_button = st.button("Predict Sales", type="primary", use_container_width=True)
    
    with col2:
        st.subheader("Quick Stats")
        st.metric("Available Items", f"{df['item_id'].nunique():,}")
        st.metric("Total Predictions", f"{len(df):,}")
        st.metric("Shops Covered", df['shop_id'].nunique())
    
    # Display results
    if predict_button and item_id_input != 0:
        st.markdown("---")
        
        with st.spinner("Calculating prediction..."):
            result = predict_sales(df, item_id_input)
        
        if result is None:
            st.error(f"Item ID {item_id_input} not found in predictions!")
            st.info("This item may not exist in the test set or has no prediction data.")
        else:
            st.success(f"Prediction for Item ID: **{item_id_input}**")
            
            # Display metrics in columns
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            
            with metric_col1:
                st.metric(
                    label="Total Predicted Sales",
                    value=f"{result['total_sales']:.2f}",
                    help="Sum of predicted sales across all shops"
                )
            
            with metric_col2:
                st.metric(
                    label="Number of Shops",
                    value=f"{result['n_shops']}",
                    help="Number of shops selling this item"
                )
            
            with metric_col3:
                st.metric(
                    label="Average per Shop",
                    value=f"{result['avg_per_shop']:.2f}",
                    help="Average sales quantity per shop"
                )
            
            # Display item information if available
            if items_info is not None:
                item_detail = items_info[items_info['item_id'] == item_id_input]
                if len(item_detail) > 0:
                    st.markdown("### Item Information")
                    st.markdown(f"**Item ID:** {item_id_input}")
                    st.markdown(f"**Category ID:** {item_detail['item_category_id'].iloc[0]}")
            
            # Display top shops
            st.markdown("### Top 5 Shops for this Item")
            
            # Create a more readable dataframe
            top_shops_display = result['top_shops'].copy()
            top_shops_display.columns = ['Shop ID', 'Predicted Sales']
            top_shops_display['Predicted Sales'] = top_shops_display['Predicted Sales'].round(2)
            top_shops_display.index = range(1, len(top_shops_display) + 1)
            
            # Display as table
            st.dataframe(
                top_shops_display,
                use_container_width=True,
                hide_index=False
            )
            
            # Visualization
            st.markdown("### Sales Distribution")
            chart_data = result['top_shops'].copy()
            chart_data.columns = ['Shop ID', 'Sales']
            chart_data['Shop ID'] = chart_data['Shop ID'].astype(str)
            
            st.bar_chart(chart_data.set_index('Shop ID'))
            
            # Additional insights
            with st.expander("View All Shops for this Item"):
                all_shops = df[df['item_id'] == item_id_input][['shop_id', 'item_cnt_month']].copy()
                all_shops.columns = ['Shop ID', 'Predicted Sales']
                all_shops['Predicted Sales'] = all_shops['Predicted Sales'].round(2)
                all_shops = all_shops.sort_values('Predicted Sales', ascending=False)
                all_shops.index = range(1, len(all_shops) + 1)
                st.dataframe(all_shops, use_container_width=True)
    
    elif predict_button and item_id_input == 0:
        st.warning("Please select a sample item or enter a valid Item ID")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 0.9em;'>
        <p>Sales Forecast System | Powered by LightGBM | DataNest Assignment 2026</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
