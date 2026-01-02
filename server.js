const express = require('express');
const cors = require('cors');
const axios = require('axios');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// Google Places API endpoint
app.get('/api/search', async (req, res) => {
  try {
    const { query, location } = req.query;
    const apiKey = process.env.GOOGLE_PLACES_API_KEY;

    if (!apiKey) {
      return res.status(500).json({ error: 'API key not configured' });
    }

    // Step 1: Text Search to find places
    const searchResponse = await axios.get(
      'https://maps.googleapis.com/maps/api/place/textsearch/json',
      {
        params: {
          query: query,
          location: location || '41.0082,28.9784', // Default to Istanbul coordinates
          radius: 50000,
          key: apiKey
        }
      }
    );

    if (searchResponse.data.status !== 'OK' && searchResponse.data.status !== 'ZERO_RESULTS') {
      throw new Error(`Google API error: ${searchResponse.data.status}`);
    }

    const places = searchResponse.data.results || [];

    // Step 2: Get detailed information for each place
    const detailedPlaces = await Promise.all(
      places.slice(0, 10).map(async (place) => {
        try {
          const detailsResponse = await axios.get(
            'https://maps.googleapis.com/maps/api/place/details/json',
            {
              params: {
                place_id: place.place_id,
                fields: 'name,formatted_address,formatted_phone_number,website,rating,reviews,user_ratings_total,opening_hours,price_level,photos',
                key: apiKey
              }
            }
          );

          const details = detailsResponse.data.result || {};
          
          return {
            name: details.name || place.name,
            address: details.formatted_address || place.formatted_address,
            phone: details.formatted_phone_number || 'N/A',
            website: details.website || 'N/A',
            rating: details.rating || place.rating || 'N/A',
            totalRatings: details.user_ratings_total || 0,
            reviews: (details.reviews || []).slice(0, 3).map(review => ({
              author: review.author_name,
              rating: review.rating,
              text: review.text,
              time: review.relative_time_description
            })),
            priceLevel: details.price_level ? '$'.repeat(details.price_level) : 'N/A',
            isOpen: details.opening_hours?.open_now,
            placeId: place.place_id
          };
        } catch (error) {
          console.error(`Error fetching details for ${place.name}:`, error.message);
          return {
            name: place.name,
            address: place.formatted_address,
            phone: 'N/A',
            website: 'N/A',
            rating: place.rating || 'N/A',
            totalRatings: 0,
            reviews: [],
            priceLevel: 'N/A',
            isOpen: null,
            placeId: place.place_id
          };
        }
      })
    );

    res.json({ places: detailedPlaces, status: 'success' });
  } catch (error) {
    console.error('Search error:', error.message);
    res.status(500).json({ 
      error: 'Failed to search restaurants', 
      message: error.message 
    });
  }
});

app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Make sure to set GOOGLE_PLACES_API_KEY in .env file`);
});