import os
import re
import datetime
from collections import defaultdict, Counter
import requests
from bs4 import BeautifulSoup

# ==========================================
# 1. THE PARENT CLASS (The Engine)
# ==========================================
class MovieLensAnalysis:
    """
    This is the parent class. It handles reading the raw text files
    so the other classes can focus on the math.
    """
    def __init__(self, path_to_the_file):
        self.path = path_to_the_file
        self.data = self._load_data()

    def _load_data(self):
        """
        Reads the first 1000 lines of the file.
        Parses CSV manually using Regex to handle commas inside quotes.
        """
        data = []
        if not os.path.exists(self.path):
            print(f"Warning: File not found at {self.path}")
            return []

        # Regex explanation:
        # Split by comma ONLY if that comma is NOT inside quotes.
        # This handles: 10,"Movie, The",Comedy
        pattern = re.compile(r',(?=(?:[^"]*"[^"]*")*[^"]*$)')

        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                header = f.readline() # Skip header
                
                count = 0
                for line in f:
                    if count >= 1000:
                        break
                    
                    line = line.strip()
                    if not line:
                        continue
                        
                    # Split the line using our smart regex
                    fields = pattern.split(line)
                    
                    # Clean up quotes around text (e.g. "Toy Story" -> Toy Story)
                    clean_fields = [field.strip('"') for field in fields]
                    
                    data.append(clean_fields)
                    count += 1
        except Exception as e:
            print(f"Error reading file {self.path}: {e}")
            
        return data

# ==========================================
# 2. THE CHILDREN CLASSES (Specific Logic)
# ==========================================

class Movies(MovieLensAnalysis):
    def dist_by_release(self):
        """
        Returns a dict where keys are years and values are counts. 
        Sorted by counts descendingly.
        """
        release_years = defaultdict(int)
        
        # Pattern to find (1995) at the end of the string
        year_pattern = re.compile(r'\((\d{4})\)')
        
        for row in self.data:
            # row structure: [movieId, title, genres]
            title = row[1]
            
            # Find the year
            match = year_pattern.search(title)
            if match:
                year = match.group(1) # Extract the numbers inside ()
                release_years[year] += 1
                
        # Sort by count (value) descending
        sorted_years = dict(sorted(release_years.items(), key=lambda item: item[1], reverse=True))
        return sorted_years
    
    def dist_by_genres(self):
        """
        Returns a dict where keys are genres and values are counts.
        Sorted by counts descendingly.
        """
        genres_count = defaultdict(int)
        
        for row in self.data:
            # row[2] is "Adventure|Animation|Children"
            genres_string = row[2]
            
            # Split by pipe
            genres = genres_string.split('|')
            
            for genre in genres:
                if genre: # Avoid empty strings
                    genres_count[genre] += 1
                    
        # Sort by count descending
        sorted_genres = dict(sorted(genres_count.items(), key=lambda item: item[1], reverse=True))
        return sorted_genres
        
    def most_genres(self, n):
        """
        Returns a dict with top-n movies with most genres.
        Sort by number of genres descending.
        """
        movie_genre_counts = {}
        
        for row in self.data:
            title = row[1]
            genres_string = row[2]
            
            # Count the genres
            count = len(genres_string.split('|'))
            movie_genre_counts[title] = count
            
        # Sort by count descending and take top n
        # .items() gives us (title, count) tuples
        sorted_movies = sorted(movie_genre_counts.items(), key=lambda item: item[1], reverse=True)
        
        # Convert the top n back to a dict
        return dict(sorted_movies[:n])
    
    #========================
    #BONUS
    #========================
    def search_by_title(self, keyword):
        """
        BONUS METHOD: Search for movies by a keyword in the title.
        Returns dict {movieId: title}
        """
        results = {}
        for row in self.data:
            movieId, title = row[0], row[1]
            if keyword.lower() in title.lower():
                results[movieId] = title
        return results
    
class Tags(MovieLensAnalysis):
    def most_words(self, n):
        """
        Returns top-n tags with most words.
        Dict: {tag: word_count}
        Sorted by word_count desc.
        Drop duplicates (if multiple users used same tag, treat it as one entry).
        """
        tag_word_counts = {}
        
        for row in self.data:
            tag = row[2]
            # Count words by splitting by space
            word_count = len(tag.split())
            tag_word_counts[tag] = word_count
            
        sorted_tags = sorted(tag_word_counts.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_tags[:n])

    def longest(self, n):
        """
        Returns top-n longest tags (by character count).
        List of tags.
        Sorted by length desc.
        """
        tag_lengths = {}
        
        for row in self.data:
            tag = row[2]
            tag_lengths[tag] = len(tag)
            
        sorted_tags = sorted(tag_lengths.items(), key=lambda item: item[1], reverse=True)
        # Return only the list of tags, not the lengths
        return [item[0] for item in sorted_tags[:n]]

    def most_words_and_longest(self, n):
        """
        Intersection of:
        1. Top-n tags with most words
        2. Top-n longest tags
        Returns a list of tags.
        """
        # Get the two lists
        # keys() gives us the tag strings from the most_words dict
        most_words_tags = list(self.most_words(n).keys())
        longest_tags = self.longest(n)
        
        # Find intersection (items present in BOTH lists)
        intersection = list(set(most_words_tags) & set(longest_tags))
        return intersection
        
    def most_popular(self, n):
        """
        Most popular tags (count occurrences).
        Dict: {tag: count}
        Sorted by count desc.
        """
        tag_counts = defaultdict(int)
        
        for row in self.data:
            tag = row[2]
            tag_counts[tag] += 1
            
        sorted_tags = sorted(tag_counts.items(), key=lambda item: item[1], reverse=True)
        return dict(sorted_tags[:n])
        
    def tags_with(self, word):
        """
        Returns unique tags that include the word.
        Sorted alphabetically.
        """
        matching_tags = set() # Use set to drop duplicates automatically
        
        for row in self.data:
            tag = row[2]
            # Case insensitive search? The prompt doesn't specify, 
            # but usually good practice. Let's stick to exact match for now 
            # unless we want to be fancy.
            if word in tag:
                matching_tags.add(tag)
                
        return sorted(list(matching_tags))
    
    # BONUS
    def avg_word_length(self):
        """
        BONUS METHOD: Calculate the average length of words used in tags.
        Returns float.
        """
        total_len = 0
        total_words = 0
        for row in self.data:
            tag = row[2]
            words = tag.split()
            for w in words:
                total_len += len(w)
                total_words += 1
        return round(total_len / total_words, 2) if total_words > 0 else 0

class Links(MovieLensAnalysis):
    def __init__(self, path_to_links, path_to_movies_csv):
        super().__init__(path_to_links)
        self.titles = {}
        try:
            with open(path_to_movies_csv, 'r', encoding='utf-8') as f:
                f.readline()
                pattern = re.compile(r',(?=(?:[^"]*"[^"]*")*[^"]*$)')
                for line in f:
                    parts = pattern.split(line.strip())
                    if len(parts) >= 2:
                        self.titles[parts[0]] = parts[1].strip('"')
        except:
            pass
        self.cache = {} 

    def _get_soup(self, imdb_id):
        if imdb_id in self.cache: return self.cache[imdb_id]
        url = f"https://www.imdb.com/title/tt{imdb_id}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                self.cache[imdb_id] = soup
                return soup
        except: pass
        return None

    def _parse_money(self, text):
        """Helper to convert '$1,000,000' to integer 1000000"""
        match = re.search(r'(\$[\d,]+)', text)
        if match:
            return int(match.group(1).replace(',', '').replace('$', ''))
        return 0

    def _parse_runtime(self, text):
        """Helper to convert '1h 30m' or '90 min' to integer minutes"""
        # Format: 1h 30m
        hm_match = re.search(r'(\d+)h\s*(\d+)m', text)
        if hm_match:
            return int(hm_match.group(1)) * 60 + int(hm_match.group(2))
        
        # Format: 1h (exactly)
        h_match = re.search(r'(\d+)h', text)
        if h_match:
            return int(h_match.group(1)) * 60
            
        # Format: 90 min
        m_match = re.search(r'(\d+)\s*min', text)
        if m_match:
            return int(m_match.group(1))
            
        return 0

    def _extract_field(self, soup, field):
        text_content = soup.get_text(separator=' ', strip=True) 
        val = "N/A"
        
        if field == 'Director':
            patterns = [
                r'Director[s]?\s*[:]?\s+([A-Z][a-z]+ [A-Z][a-z]+)',
                r'Directed by\s+([A-Z][a-z]+ [A-Z][a-z]+)'
            ]
            for pat in patterns:
                match = re.search(pat, text_content)
                if match:
                    val = match.group(1).strip()
                    break
                    
        elif field == 'Budget':
            # Look for Budget section specifically
            if "Budget" in text_content:
                # Extract substring to reduce false positives
                idx = text_content.find("Budget")
                snippet = text_content[idx:idx+50]
                money = self._parse_money(snippet)
                if money > 0: val = str(money)

        elif field == 'Gross':
            # Look for Cumulative Worldwide Gross
            patterns = ["Cumulative Worldwide Gross", "Gross worldwide"]
            for pat in patterns:
                if pat in text_content:
                    idx = text_content.find(pat)
                    snippet = text_content[idx:idx+50]
                    money = self._parse_money(snippet)
                    if money > 0: 
                        val = str(money)
                        break

        elif field == 'Runtime':
            # Look for runtime pattern
            val_mins = self._parse_runtime(text_content)
            if val_mins > 0:
                val = f"{val_mins} min" # Store as string for display, parse later if needed

        return val

    def get_imdb(self, list_of_movies, list_of_fields):
        results = []
        for movieId in list_of_movies:
            row = next((r for r in self.data if r[0] == movieId), None)
            if not row: continue
            imdbId = row[1]
            soup = self._get_soup(imdbId)
            row_result = [movieId]
            if soup:
                for field in list_of_fields:
                    val = self._extract_field(soup, field)
                    row_result.append(val)
            else:
                row_result.extend(["N/A"] * len(list_of_fields))
            results.append(row_result)
        return sorted(results, key=lambda x: x[0], reverse=True)

    def top_directors(self, n):
        director_counts = defaultdict(int)
        count = 0
        for row in self.data:
            if count >= 10: break # Scrape limit
            movieId, imdbId = row[0], row[1]
            soup = self._get_soup(imdbId)
            if soup:
                director = self._extract_field(soup, 'Director')
                if director != "N/A":
                    director_counts[director] += 1
            count += 1
        return dict(sorted(director_counts.items(), key=lambda x: x[1], reverse=True)[:n])

    def most_expensive(self, n):
        movie_budgets = {}
        count = 0
        for row in self.data:
            if count >= 10: break
            movieId, imdbId = row[0], row[1]
            soup = self._get_soup(imdbId)
            if soup:
                budget_str = self._extract_field(soup, 'Budget')
                if budget_str != "N/A":
                    title = self.titles.get(movieId, f"Movie {movieId}")
                    movie_budgets[title] = int(budget_str)
            count += 1
        return dict(sorted(movie_budgets.items(), key=lambda x: x[1], reverse=True)[:n])
    
    def most_profitable(self, n):
        """
        Gross - Budget.
        """
        profits = {}
        count = 0
        for row in self.data:
            if count >= 10: break
            movieId, imdbId = row[0], row[1]
            soup = self._get_soup(imdbId)
            if soup:
                budget = self._extract_field(soup, 'Budget')
                gross = self._extract_field(soup, 'Gross')
                
                if budget != "N/A" and gross != "N/A":
                    profit = int(gross) - int(budget)
                    title = self.titles.get(movieId, f"Movie {movieId}")
                    profits[title] = profit
            count += 1
        return dict(sorted(profits.items(), key=lambda x: x[1], reverse=True)[:n])

    def longest(self, n):
        """
        Top n movies by runtime.
        """
        runtimes = {}
        count = 0
        for row in self.data:
            if count >= 10: break
            movieId, imdbId = row[0], row[1]
            soup = self._get_soup(imdbId)
            if soup:
                rt_str = self._extract_field(soup, 'Runtime')
                if rt_str != "N/A":
                    # Convert back to int for sorting
                    mins = int(rt_str.split()[0])
                    title = self.titles.get(movieId, f"Movie {movieId}")
                    runtimes[title] = mins
            count += 1
        # Sort by value (minutes) descending
        sorted_rt = sorted(runtimes.items(), key=lambda x: x[1], reverse=True)[:n]
        # Return format "120 min" in the value? Or just int?
        # Prompt says "values are their runtime". Let's return formatted string for report
        result = {}
        for k, v in sorted_rt:
            result[k] = f"{v} min"
        return result

    def top_cost_per_minute(self, n):
        """
        Budget / Runtime.
        """
        costs = {}
        count = 0
        for row in self.data:
            if count >= 10: break
            movieId, imdbId = row[0], row[1]
            soup = self._get_soup(imdbId)
            if soup:
                budget_str = self._extract_field(soup, 'Budget')
                rt_str = self._extract_field(soup, 'Runtime')
                
                if budget_str != "N/A" and rt_str != "N/A":
                    budget = int(budget_str)
                    mins = int(rt_str.split()[0])
                    if mins > 0:
                        cpm = budget / mins
                        title = self.titles.get(movieId, f"Movie {movieId}")
                        costs[title] = round(cpm, 2)
            count += 1
        return dict(sorted(costs.items(), key=lambda x: x[1], reverse=True)[:n])

    # ==========================
    # BONUS METHOD
    # ==========================
    def top_grossing(self, n):
        """
        BONUS: Top n movies by total worldwide gross revenue.
        """
        grosses = {}
        count = 0
        for row in self.data:
            if count >= 10: break
            movieId, imdbId = row[0], row[1]
            soup = self._get_soup(imdbId)
            if soup:
                gross_str = self._extract_field(soup, 'Gross')
                if gross_str != "N/A":
                    title = self.titles.get(movieId, f"Movie {movieId}")
                    grosses[title] = int(gross_str)
            count += 1
        return dict(sorted(grosses.items(), key=lambda x: x[1], reverse=True)[:n])

import statistics

class Ratings(MovieLensAnalysis):
    def __init__(self, path_to_ratings, movies_object):
        """
        path_to_ratings: Path to ratings.csv
        movies_object: An instance of the Movies class (so we can look up titles)
        """
        super().__init__(path_to_ratings)
        
        # Create a helper dict to map movieId -> Title
        # movies_object.data is a list of [movieId, title, genres]
        self.titles = {row[0]: row[1] for row in movies_object.data}
        
        # Initialize the nested classes, passing the necessary data down to them
        self.movies = self.Movies(self.data, self.titles)
        self.users = self.Users(self.data, self.titles)

    class Movies:
        def __init__(self, ratings_data, titles_dict):
            self.data = ratings_data
            self.titles = titles_dict

        def dist_by_year(self):
            """
            Distribution of ratings by year (extracted from timestamp).
            Sorted by year ascending.
            """
            year_counts = defaultdict(int)
            for row in self.data:
                timestamp = int(row[3])
                # Convert timestamp to year
                dt = datetime.datetime.fromtimestamp(timestamp)
                year_counts[dt.year] += 1
                
            return dict(sorted(year_counts.items())) # Sort by key (year)

        def dist_by_rating(self):
            """
            Distribution of ratings by rating value.
            Sorted by rating ascending.
            """
            rating_counts = defaultdict(int)
            for row in self.data:
                rating = float(row[2])
                rating_counts[rating] += 1
                
            return dict(sorted(rating_counts.items()))

        def top_by_num_of_ratings(self, n):
            """
            Top n movies by number of ratings.
            Returns {Title: Count}
            """
            movie_counts = defaultdict(int)
            for row in self.data:
                movieId = row[1]
                movie_counts[movieId] += 1
                
            # Sort by count desc
            sorted_movies = sorted(movie_counts.items(), key=lambda x: x[1], reverse=True)
            
            # Convert ID to Title and return top n
            result = {}
            for movieId, count in sorted_movies[:n]:
                # If movie not in our limited 1000-line movies file, use ID
                title = self.titles.get(movieId, str(movieId)) 
                result[title] = count
            return result

        def top_by_ratings(self, n, metric='average'):
            """
            Top n movies by average or median rating.
            """
            # 1. Group ratings by movie
            movie_ratings = defaultdict(list)
            for row in self.data:
                movieId = row[1]
                rating = float(row[2])
                movie_ratings[movieId].append(rating)
            
            # 2. Calculate metric for each movie
            movie_metrics = {}
            for movieId, ratings_list in movie_ratings.items():
                if metric == 'average':
                    val = statistics.mean(ratings_list)
                elif metric == 'median':
                    val = statistics.median(ratings_list)
                else:
                    val = 0
                movie_metrics[movieId] = val
                
            # 3. Sort
            sorted_movies = sorted(movie_metrics.items(), key=lambda x: x[1], reverse=True)
            
            # 4. Format result
            result = {}
            for movieId, val in sorted_movies[:n]:
                title = self.titles.get(movieId, str(movieId))
                result[title] = round(val, 2)
            return result

        def top_controversial(self, n):
            """
            Top n movies by variance of ratings.
            """
            movie_ratings = defaultdict(list)
            for row in self.data:
                movieId = row[1]
                rating = float(row[2])
                movie_ratings[movieId].append(rating)
                
            movie_variance = {}
            for movieId, ratings_list in movie_ratings.items():
                if len(ratings_list) > 1:
                    val = statistics.variance(ratings_list)
                else:
                    val = 0 # Variance needs at least 2 data points
                movie_variance[movieId] = val
                
            sorted_movies = sorted(movie_variance.items(), key=lambda x: x[1], reverse=True)
            
            result = {}
            for movieId, val in sorted_movies[:n]:
                title = self.titles.get(movieId, str(movieId))
                result[title] = round(val, 2)
            return result

    class Users(Movies):
        """
        Inherits from Movies but analyzes Users.
        We override the logic to group by UserID instead of MovieID.
        """
        
        # Helper to get user distribution stats
        def _get_user_stats(self):
            user_ratings = defaultdict(list)
            for row in self.data:
                userId = row[0]
                rating = float(row[2])
                user_ratings[userId].append(rating)
            return user_ratings

        def dist_by_ratings_number(self):
            """
            Distribution of users by number of ratings.
            This is slightly different: we want dict {userId: count_of_ratings} 
            OR distribution of counts {count: num_users_with_this_count}?
            
            Prompt: "returns the distribution of users by the number of ratings made by them"
            Usually implies: {count_of_ratings: number_of_users} 
            (e.g., 5 users rated 10 movies -> {10: 5})
            Let's assume simple {userId: count} sorted descending first based on other methods.
            """
            user_counts = defaultdict(int)
            for row in self.data:
                userId = row[0]
                user_counts[userId] += 1
            
            # Sorting by number of ratings descending
            return dict(sorted(user_counts.items(), key=lambda x: x[1], reverse=True))

        def dist_by_ratings_average(self):
            """
            Distribution of users by average rating.
            Returns {userId: average_rating} sorted desc.
            """
            user_stats = self._get_user_stats()
            user_avg = {}
            for userId, ratings in user_stats.items():
                user_avg[userId] = statistics.mean(ratings)
                
            return dict(sorted(user_avg.items(), key=lambda x: x[1], reverse=True))

        def dist_by_ratings_variance(self):
            """
            Top users with biggest variance.
            """
            user_stats = self._get_user_stats()
            user_var = {}
            for userId, ratings in user_stats.items():
                if len(ratings) > 1:
                    user_var[userId] = statistics.variance(ratings)
                else:
                    user_var[userId] = 0
            
            # Since the prompt asks for "top-n" in the description but this method signature 
            # in the skeleton didn't have 'n', we return the full sorted dict.
            return dict(sorted(user_var.items(), key=lambda x: x[1], reverse=True))
# ==========================================
# 3. THE TESTS CLASS
# ==========================================
class Tests:
    """
    Comprehensive tests for the MovieLens modules.
    """
    def test_links(self):
        # We assume internet connection and strict limit of 5 to avoid timeouts
        l = Links('../datasets/links.csv', '../datasets/movies.csv')

        print("Testing Links...")
        
        # Test get_imdb structure
        res_list = l.get_imdb(['1'], ['Director', 'Budget'])
        assert isinstance(res_list, list)
        assert len(res_list) > 0
        assert len(res_list[0]) == 3 # ID + Dir + Bud
        
        # Test most_expensive
        res_exp = l.most_expensive(3)
        assert isinstance(res_exp, dict)
        # Check sorting
        vals = list(res_exp.values())
        assert vals == sorted(vals, reverse=True)
        
        # Test most_profitable
        res_prof = l.most_profitable(3)
        assert isinstance(res_prof, dict)
        
        # Test longest
        res_long = l.longest(3)
        assert isinstance(res_long, dict)
        
        # Test top_cost_per_minute
        res_cpm = l.top_cost_per_minute(3)
        assert isinstance(res_cpm, dict)
        
        # Test BONUS: top_grossing
        res_gross = l.top_grossing(3)
        assert isinstance(res_gross, dict)
        vals_gross = list(res_gross.values())
        assert vals_gross == sorted(vals_gross, reverse=True)

    def test_movies(self):
        # Initialize
        m = Movies('../datasets/movies.csv')

        print("Testing Movies...")
        
        # Test dist_by_release
        res = m.dist_by_release()
        assert isinstance(res, dict)
        # Check sorting (descending values)
        vals = list(res.values())
        assert vals == sorted(vals, reverse=True)
        
        # Test dist_by_genres
        res = m.dist_by_genres()
        assert isinstance(res, dict)
        vals = list(res.values())
        assert vals == sorted(vals, reverse=True)
        
        # Test most_genres
        res = m.most_genres(5)
        assert isinstance(res, dict)
        assert len(res) <= 5

        # Bonus
        res = m.search_by_title("Toy Story")
        assert isinstance(res, dict)
        assert len(res) > 0
        first_title = list(res.values())[0]
        assert "Toy Story" in first_title

    def test_tags(self):
            # Initialize
            t = Tags('../datasets/tags.csv')
            
            print("Testing Tags...")

            # 1. most_words: Sorted by Word Count (Value) Descending
            res = t.most_words(5)
            assert isinstance(res, dict)
            assert len(res) <= 5
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)
            
            # 2. longest: List of tags, sorted by length Descending
            res = t.longest(5)
            assert isinstance(res, list)
            assert len(res) <= 5
            # Check sorting by length of string
            if len(res) > 1:
                assert len(res[0]) >= len(res[1])
            
            # 3. most_words_and_longest: Intersection (List)
            # We use a larger N to ensure overlap possibility
            res = t.most_words_and_longest(200)
            assert isinstance(res, list)
            # Result cannot be larger than N
            assert len(res) <= 200
            
            # 4. most_popular: Sorted by Count (Value) Descending
            res = t.most_popular(5)
            assert isinstance(res, dict)
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)
            
            # 5. tags_with: Alphabetical List containing the word
            keyword = 'funny'
            res = t.tags_with(keyword)
            assert isinstance(res, list)
            if len(res) > 0:
                # Check if the word is actually inside the tag
                assert keyword in res[0]
                # Check alphabetical sorting
                assert res == sorted(res)

            # 6. avg_word_length (Bonus)
            res = t.avg_word_length()
            assert isinstance(res, float)
            assert res > 0

    def test_ratings(self):
            # Initialize (using your specific paths)
            m = Movies('../datasets/movies.csv')
            r = Ratings('../datasets/ratings.csv', m)
            
            print("Testing Ratings.Movies...")
            
            # 1. dist_by_year: Should be sorted by Year (Key) Ascending
            res = r.movies.dist_by_year()
            assert isinstance(res, dict)
            keys = list(res.keys())
            assert keys == sorted(keys)

            # 2. dist_by_rating: Should be sorted by Rating Score (Key) Ascending
            res = r.movies.dist_by_rating()
            assert isinstance(res, dict)
            keys = list(res.keys())
            assert keys == sorted(keys)

            # 3. top_by_num_of_ratings: Sorted by Count (Value) Descending
            res = r.movies.top_by_num_of_ratings(5)
            assert isinstance(res, dict)
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)

            # 4. top_by_ratings: Sorted by Average (Value) Descending
            res = r.movies.top_by_ratings(5, metric='average')
            assert isinstance(res, dict)
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)

            # 5. top_controversial: Sorted by Variance (Value) Descending
            res = r.movies.top_controversial(5)
            assert isinstance(res, dict)
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)
            print("Testing Ratings.Users...")

            # BONUS
            # 6. dist_by_ratings_number: Sorted by Count (Value) Descending
            res = r.users.dist_by_ratings_number()
            assert isinstance(res, dict)
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)

            # 7. dist_by_ratings_average: Sorted by Average (Value) Descending
            res = r.users.dist_by_ratings_average()
            assert isinstance(res, dict)
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)

            # 8. dist_by_ratings_variance: Sorted by Variance (Value) Descending
            res = r.users.dist_by_ratings_variance()
            assert isinstance(res, dict)
            vals = list(res.values())
            assert vals == sorted(vals, reverse=True)