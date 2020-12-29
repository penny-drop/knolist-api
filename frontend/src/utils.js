import {Alert} from 'rsuite';

export default class Utils {
    constructor(jwt, baseUrl) {
        this.jwt = jwt;
        this.baseUrl = baseUrl;
    }

    /**
     * Used to make standard requests to the Knolist API. Includes authorization.
     * @param endpoint The request endpoint (including the first slash). E.g., "/projects"
     * @param params The request parameters that would be used in the fetch call.
     * @returns {Promise<{body: any, status: number}>}
     */
    makeHttpRequest = async (endpoint, params = {}) => {
        const url = this.baseUrl + endpoint;
        // Add authorization to the request
        if (!params.hasOwnProperty("headers")) {
            params["headers"] = {};
        }
        params["headers"]["Authorization"] = "Bearer " + this.jwt;

        // Make request
        const response = await fetch(url, params);
        const responseStatus = response.status;
        const responseBody = await response.json();
        if (!responseBody.success) {
            Alert.error("Something went wrong!");
        }
        return {
            status: responseStatus,
            body: responseBody
        };
    }

    /**
     * Trims a function for leading or trailing whitespace.
     * Based on https://stackoverflow.com/questions/8517089/js-search-in-object-values
     * @param s
     * @returns {string}
     */
    trimString = (s) => {
        let l=0, r=s.length -1;
        while(l < s.length && s[l] === ' ') l++;
        while(r > l && s[r] === ' ') r-=1;
        return s.substring(l, r+1);
    };
}