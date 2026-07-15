class MarketplaceCalculator:
    """
    Kelas utilitas untuk menghitung harga jual di berbagai marketplace
    berdasarkan target bersih (net) atau target bayar pembeli.
    """
    
    @staticmethod
    def get_u7buy_listing_price(target_buyer_price: float) -> float:
        """
        Di U7BUY, pembeli menanggung pajak ~10%.
        Jika kita ingin pembeli membayar tepat $X, maka harga yang kita set (listing) 
        adalah X / 1.10. Pendapatan bersih kita = Harga Listing.
        """
        return target_buyer_price / 1.10

    @staticmethod
    def get_eldorado_listing_price(target_net_income: float, is_item: bool = False) -> float:
        """
        Di Eldorado, penjual menanggung pajak dari harga listing.
        Boosting = 10% fee. Item = 15% fee.
        Jika kita ingin bersih $X, maka: Listing = X / (1 - fee_rate)
        """
        fee_rate = 0.15 if is_item else 0.10
        return target_net_income / (1.0 - fee_rate)
        
    @staticmethod
    def calculate_all_metrics(marketplace: str, category: str, target: float) -> dict:
        """Fungsi helper untuk mendapatkan rincian lengkap dari suatu kalkulasi"""
        result = {
            "target": target,
            "listing_price": 0.0,
            "net_income": 0.0,
            "buyer_pays": 0.0
        }
        
        if marketplace == "U7BUY":
            listing = MarketplaceCalculator.get_u7buy_listing_price(target)
            result["listing_price"] = listing
            result["net_income"] = listing
            result["buyer_pays"] = target
            
        elif marketplace == "Eldorado":
            is_item = (category.lower() == "item")
            listing = MarketplaceCalculator.get_eldorado_listing_price(target, is_item)
            fee = 0.15 if is_item else 0.10
            
            result["listing_price"] = listing
            result["net_income"] = target
            # Asumsi standar pembeli Eldorado juga kena fee gateway, tapi untuk 
            # display seller, buyer_pays biasanya setara listing price + fee tambahan (opsional)
            result["buyer_pays"] = listing 
            
        return result