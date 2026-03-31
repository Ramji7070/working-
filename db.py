import os

MONGO_URL = os.environ.get("MONGO_URL")

class LocalDB:
    def __init__(self):
        self.users = set()
        self.admins = set()

    def is_user_authorized(self, *a, **k): return True
    def is_admin(self, *a, **k): return True

    def __getattr__(self, name):
        return lambda *a, **k: True


try:
    if MONGO_URL:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URL)
        db = client["botdb"]
        print("✅ MongoDB Connected")
    else:
        raise Exception("No MONGO_URL")

except Exception as e:
    print("❌ Mongo Failed → Using Local DB")

    class Database:
        def __init__(self):
            self.local = LocalDB()

        def __getattr__(self, name):
            return getattr(self.local, name)

    db = Database()        try:
            # Single field index for settings
            self.settings.create_index(
                [("user_id", 1)],
                unique=True,
                name="user_settings"
            )
            index_results.append("settings index")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Could not create settings index: {str(e)}{Style.RESET_ALL}")

        try:
            # TTL index for expiry dates
            self.users.create_index(
                "expiry_date",
                name="user_expiry",
                expireAfterSeconds=0  # Documents will be deleted at expiry_date
            )
            index_results.append("expiry TTL index")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠ Could not create expiry index: {str(e)}{Style.RESET_ALL}")
            
        return index_results

    def _migrate_existing_users(self):
        """Migrate existing users to new schema if needed"""
        try:
            update_result = self.users.update_many(
                {"bot_username": {"$exists": False}},
                {"$set": {"bot_username": "ITsGOLU_UPLOADER"}}
            )
            
            if update_result.modified_count > 0:
                print(f"{Fore.YELLOW}⚠ Migrated {update_result.modified_count} users to new schema{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}⚠ Could not migrate users: {str(e)}{Style.RESET_ALL}")

    def get_user(self, user_id: int, bot_username: str = "ITsGOLU_UPLOADER") -> Optional[dict]:
        """
        Retrieve a user document
        
        Args:
            user_id: Telegram user ID
            bot_username: Bot username (default: "ITsGOLU_UPLOADER")
            
        Returns:
            User document or None if not found
        """
        try:
            return self.users.find_one({
                "user_id": user_id,
                "bot_username": bot_username
            })
        except Exception as e:
            print(f"{Fore.RED}Error getting user {user_id}: {str(e)}{Style.RESET_ALL}")
            return None

    def is_user_authorized(self, user_id: int, bot_username: str = "ITsGOLU_UPLOADER") -> bool:
        """
        Check if user is authorized (admin or has valid subscription)
        
        Args:
            user_id: Telegram user ID
            bot_username: Bot username
            
        Returns:
            True if authorized, False otherwise
        """
        try:
            # First check if user is admin/owner
            if user_id == OWNER_ID or user_id in ADMINS:
                return True
                
            # Then check subscription status
            user = self.get_user(user_id, bot_username)
            if not user:
                return False
                
            expiry = user.get('expiry_date')
            if not expiry:
                return False
                
            # Handle string expiry dates (backward compatibility)
            if isinstance(expiry, str):
                expiry = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")
                
            return expiry > datetime.now()
            
        except Exception as e:
            print(f"{Fore.RED}Authorization error for {user_id}: {str(e)}{Style.RESET_ALL}")
            return False

    def add_user(self, user_id: int, name: str, days: int, 
                bot_username: str = "ITsGOLU_UPLOADER") -> tuple[bool, Optional[datetime]]:
        """
        Add or update a user in the database
        
        Args:
            user_id: Telegram user ID
            name: User's display name
            days: Subscription duration in days
            bot_username: Bot username
            
        Returns:
            Tuple of (success, expiry_date)
        """
        try:
            expiry_date = datetime.now() + timedelta(days=days)
            update_result = self.users.update_one(
                {"user_id": user_id, "bot_username": bot_username},
                {"$set": {
                    "name": name,
                    "expiry_date": expiry_date,
                    "added_date": datetime.now(),
                    "last_updated": datetime.now()
                }},
                upsert=True
            )
            
            if update_result.upserted_id or update_result.modified_count > 0:
                return True, expiry_date
            return False, None
            
        except Exception as e:
            print(f"{Fore.RED}Add user error for {user_id}: {str(e)}{Style.RESET_ALL}")
            return False, None

    def remove_user(self, user_id: int, bot_username: str = "ITsGOLU_UPLOADER") -> bool:
        """
        Remove a user from the database
        
        Args:
            user_id: Telegram user ID
            bot_username: Bot username
            
        Returns:
            True if user was deleted, False otherwise
        """
        try:
            result = self.users.delete_one({
                "user_id": user_id,
                "bot_username": bot_username
            })
            return result.deleted_count > 0
        except Exception as e:
            print(f"{Fore.RED}Remove user error for {user_id}: {str(e)}{Style.RESET_ALL}")
            return False

    def list_users(self, bot_username: str = "ITsGOLU_UPLOADER") -> List[dict]:
        """
        List all users for a specific bot
        
        Args:
            bot_username: Bot username to filter by
            
        Returns:
            List of user documents
        """
        try:
            return list(self.users.find(
                {"bot_username": bot_username},
                {"_id": 0, "name": 1, "user_id": 1, "expiry_date": 1}
            ))
        except Exception as e:
            print(f"{Fore.RED}List users error: {str(e)}{Style.RESET_ALL}")
            return []

    def is_admin(self, user_id: int) -> bool:
        """
        Check if user is admin or owner
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            True if admin/owner, False otherwise
        """
        try:
            is_admin = user_id == OWNER_ID or user_id in ADMINS
            if is_admin:
                print(f"{Fore.GREEN}✓ Admin/Owner {user_id} verified{Style.RESET_ALL}")
            return is_admin
        except Exception as e:
            print(f"{Fore.RED}Admin check error: {str(e)}{Style.RESET_ALL}")
            return False
    def get_log_channel(self, bot_username: str):
        """Get the log channel ID for a specific bot"""
        try:
            settings = self.db.bot_settings.find_one({"bot_username": bot_username})
            if settings and 'log_channel' in settings:
                return settings['log_channel']
            return None
        except Exception as e:
            print(f"Error getting log channel: {str(e)}")
            return None

    def set_log_channel(self, bot_username: str, channel_id: int):
        """Set the log channel ID for a specific bot"""
        try:
            self.db.bot_settings.update_one(
                {"bot_username": bot_username},
                {"$set": {"log_channel": channel_id}},
                upsert=True
            )
            return True
        except Exception as e:
            print(f"Error setting log channel: {str(e)}")
            return False
            
    def list_bot_usernames(self) -> List[str]:
        """
        Get distinct bot usernames from users collection
        
        Returns:
            List of bot usernames
        """
        try:
            usernames = self.users.distinct("bot_username")
            return usernames if usernames else ["ITsGOLU_UPLOADER"]
        except Exception as e:
            print(f"{Fore.RED}List bot usernames error: {str(e)}{Style.RESET_ALL}")
            return ["ITsGOLU_UPLOADER"]

    async def cleanup_expired_users(self, bot) -> int:
        """
        Clean up expired users and notify them
        
        Args:
            bot: Telegram bot instance
            
        Returns:
            Number of users removed
        """
        try:
            current_time = datetime.now()
            expired_users = self.users.find({
                "expiry_date": {"$lt": current_time},
                "user_id": {"$nin": [OWNER_ID] + ADMINS}
            })

            removed_count = 0
            for user in expired_users:
                try:
                    # Notify user
                    await bot.send_message(
                        user["user_id"],
                        f"**⚠️ Your subscription has expired!**\n\n"
                        f"• Name: {user['name']}\n"
                        f"• Expired on: {user['expiry_date'].strftime('%d-%m-%Y')}\n\n"
                        f"Contact admin to renew your subscription."
                    )
                    
                    # Remove user
                    self.users.delete_one({"_id": user["_id"]})
                    removed_count += 1

                    # Log to admins
                    log_msg = (
                        f"**🚫 Removed Expired User**\n\n"
                        f"• Name: {user['name']}\n"
                        f"• ID: {user['user_id']}\n"
                        f"• Expired on: {user['expiry_date'].strftime('%d-%m-%Y')}"
                    )
                    for admin in ADMINS + [OWNER_ID]:
                        try:
                            await bot.send_message(admin, log_msg)
                        except:
                            continue

                except Exception as e:
                    print(f"{Fore.YELLOW}Error processing user {user['user_id']}: {str(e)}{Style.RESET_ALL}")
                    continue

            return removed_count

        except Exception as e:
            print(f"{Fore.RED}Cleanup error: {str(e)}{Style.RESET_ALL}")
            return 0

    def get_user_expiry_info(self, user_id: int, bot_username: str = "ITsGOLU_UPLOADER") -> Optional[dict]:
        """
        Get user's subscription expiry information
        
        Args:
            user_id: Telegram user ID
            bot_username: Bot username
            
        Returns:
            Dictionary with expiry info or None if not found
        """
        try:
            user = self.get_user(user_id, bot_username)
            if not user:
                return None

            expiry = user.get('expiry_date')
            if not expiry:
                return None

            if isinstance(expiry, str):
                expiry = datetime.strptime(expiry, "%Y-%m-%d %H:%M:%S")

            days_left = (expiry - datetime.now()).days

            return {
                "name": user.get('name', 'Unknown'),
                "user_id": user_id,
                "expiry_date": expiry.strftime("%d-%m-%Y"),
                "days_left": days_left,
                "added_date": user.get('added_date', 'Unknown'),
                "is_active": days_left > 0
            }

        except Exception as e:
            print(f"{Fore.RED}Get expiry info error for {user_id}: {str(e)}{Style.RESET_ALL}")
            return None

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print(f"{Fore.YELLOW}✓ MongoDB connection closed{Style.RESET_ALL}")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - close connection"""
        self.close()

# 🔰 Startup Message
print(f"\n{Fore.CYAN}{'='*50}")
print(f"🤖 Initializing ITsGOLU_UPLOADER Bot Database")
print(f"{'='*50}{Style.RESET_ALL}\n")

# 🔌 Connect to DB with error handling
try:
    db = Database(max_retries=3, retry_delay=2)
except Exception as e:
    print(f"{Fore.RED}✕ Fatal Error: DB initialization failed!{Style.RESET_ALL}")
    raise
